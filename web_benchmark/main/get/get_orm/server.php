<?php

require __DIR__ . '/vendor/autoload.php';

use Illuminate\Database\Capsule\Manager as Capsule;
use Illuminate\Database\Eloquent\Model;

class User extends Model {
    public $timestamps = false;
    protected $table = 'users';
    protected $fillable = ['name', 'email'];
    public function profile() {
        return $this->hasOne(Profile::class, 'user_id');
    }
    public function orders() {
        return $this->hasMany(Order::class, 'user_id');
    }
}

class Profile extends Model {
    public $timestamps = false;
    protected $table = 'profiles';
    protected $fillable = ['user_id', 'age', 'address'];
    public function user() {
        return $this->belongsTo(User::class, 'user_id');
    }
}

class Order extends Model {
    public $timestamps = false;
    protected $table = 'orders';
    protected $fillable = ['user_id', 'total_amount'];
    public function user() {
        return $this->belongsTo(User::class, 'user_id');
    }
    public function orderItems() {
        return $this->hasMany(OrderItem::class, 'order_id');
    }
}

class OrderItem extends Model {
    public $timestamps = false;
    protected $table = 'order_items';
    protected $fillable = ['order_id', 'product_name', 'price'];
    public function order() {
        return $this->belongsTo(Order::class, 'order_id');
    }
}

class BenchmarkServer {
    private $dbPool;

    public function __construct() {
        $this->setupEloquent();
        $this->initDatabase();
    }

    private function setupEloquent() {
        $capsule = new Capsule();
        $capsule->addConnection([
            'driver' => 'mysql',
            'host' => '127.0.0.1',
            'port' => 3306,
            'database' => 'benchmark_db',
            'username' => 'admin',
            'password' => 'secret',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
        ]);

        $capsule->setAsGlobal();
        $capsule->bootEloquent();
    }

    private function initDatabase() {
        $dsn = 'mysql:host=127.0.0.1;port=3306';
        $pdo = new PDO($dsn, 'admin', 'secret', [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $pdo->exec('CREATE DATABASE IF NOT EXISTS benchmark_db');
        $pdo->exec('USE benchmark_db');

        $pdo->exec("CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )");

        $pdo->exec("CREATE TABLE IF NOT EXISTS profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            age INT,
            address VARCHAR(255)
        )");

        $pdo->exec("CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            total_amount DECIMAL(10, 2)
        )");

        $pdo->exec("CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product_name VARCHAR(100),
            price DECIMAL(10, 2)
        )");

        $count = $pdo->query('SELECT COUNT(*) FROM users')->fetchColumn();
        if ($count == 0) {
            $this->insertMockData($pdo);
        }

        $config = (new Swoole\Database\PDOConfig())
            ->withDriver('mysql')
            ->withHost('127.0.0.1')
            ->withPort(3306)
            ->withUsername('admin')
            ->withPassword('secret')
            ->withDbname('benchmark_db')
            ->withCharset('utf8mb4');

        $this->dbPool = new Swoole\Database\PDOPool($config, 100);
    }

    private function insertMockData(PDO $pdo) {
        $pdo->beginTransaction();
        try {
            for ($i = 1; $i <= 10000; $i++) {
                $pdo->exec("INSERT INTO users (name, email) VALUES ('User{$i}', 'user{$i}@example.com')");
                $pdo->exec("INSERT INTO profiles (user_id, age, address) VALUES ({$i}, " . (20 + ($i % 50)) . ", 'Address {$i}')");
                $pdo->exec("INSERT INTO orders (user_id, total_amount) VALUES ({$i}, " . (100.0 + $i) . ")");

                if ($i % 10 == 0) {
                    for ($j = 0; $j < 5; $j++) {
                        $pdo->exec("INSERT INTO order_items (order_id, product_name, price) VALUES ({$i}, 'Product{$j}', " . (10.0 + $j) . ")");
                    }
                }
            }
            $pdo->commit();
        } catch (Exception $e) {
            $pdo->rollBack();
            throw $e;
        }
    }

    public function start() {
        $server = new Swoole\Http\Server('0.0.0.0', 8003);
        $server->set([
            'worker_num' =>100,
            'enable_coroutine' => false,
            'log_file' => '/dev/null',
        ]);

        $server->on('workerStart', function ($server, $workerId) {
            $pdo = new PDO('mysql:host=127.0.0.1;port=3306;dbname=benchmark_db;charset=utf8mb4', 'admin', 'secret', [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ]);
                Capsule::connection()->setPdo($pdo);
        });

        $server->on('Request', function ($request, $response) {
            $path = $request->server['request_uri'];
            $pdo = $this->dbPool->get();
            Capsule::connection()->setPdo($pdo);

            try {
                if ($path === '/') {
                    $result = ['status' => 'success', 'message' => 'Hello Benchmark'];
                } elseif ($path === '/orm/1table') {
                    $result = User::limit(100)->get()->toArray();
                } elseif ($path === '/orm/2join') {
                    $result = User::select('users.name', 'profiles.age')
                        ->join('profiles', 'users.id', '=', 'profiles.user_id')
                        ->limit(100)
                        ->get()
                        ->toArray();
                } elseif ($path === '/orm/3join') {
                    $result = User::select('users.name', 'profiles.age', 'orders.total_amount')
                        ->join('profiles', 'users.id', '=', 'profiles.user_id')
                        ->join('orders', 'users.id', '=', 'orders.user_id')
                        ->limit(100)
                        ->get()
                        ->toArray();
                } elseif ($path === '/orm/4join') {
                    $result = User::select('users.name', 'profiles.age', 'orders.total_amount', 'order_items.product_name')
                        ->join('profiles', 'users.id', '=', 'profiles.user_id')
                        ->join('orders', 'users.id', '=', 'orders.user_id')
                        ->join('order_items', 'orders.id', '=', 'order_items.order_id')
                        ->limit(100)
                        ->get()
                        ->toArray();
                } else {
                    $response->status(404);
                    $result = ['error' => 'Not found'];
                }

                $response->header('Content-Type', 'application/json');
                $response->end(json_encode($result));
            } finally {
                $this->dbPool->put($pdo);
            }
        });

        $server->start();
    }
}

$server = new BenchmarkServer();
$server->start();
