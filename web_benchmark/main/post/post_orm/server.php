<?php
require 'vendor/autoload.php';

use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;
use Illuminate\Database\Capsule\Manager as Capsule;
use Illuminate\Database\Eloquent\Model;

// Eloquent Models
class User extends Model {
    protected $table = 'users';
    public $timestamps = false;
    protected $guarded = [];
}
class Profile extends Model {
    protected $table = 'profiles';
    public $timestamps = false;
    protected $guarded = [];
}
class Order extends Model {
    protected $table = 'orders';
    public $timestamps = false;
    protected $guarded = [];
}
class OrderItem extends Model {
    protected $table = 'order_items';
    public $timestamps = false;
    protected $guarded = [];
}

class BenchmarkOrmServer {
    public function start() {
        $http = new Server('0.0.0.0', 8003);
        $http->set(['worker_num' => swoole_cpu_num(), 'log_file' => '/dev/null']);
        
        // Setup Eloquent per worker
        $http->on('WorkerStart', function ($server, $workerId) {
            $capsule = new Capsule;
            $capsule->addConnection([
                'driver'    => 'mysql',
                'host'      => '127.0.0.1',
                'database'  => 'benchmark_db',
                'username'  => 'admin',
                'password'  => 'secret',
                'charset'   => 'utf8mb4',
                'collation' => 'utf8mb4_unicode_ci',
                'prefix'    => '',
                'pool'      => ['max_connections' => 10] // Connection limit
            ]);
            $capsule->setAsGlobal();
            $capsule->bootEloquent();
        });

        $http->on('Request', function (Request $request, Response $response) {
            $path = $request->server['path_info'];
            
            if ($path === '/orm/post/1table') {
                $this->handle1Table($response);
            } elseif ($path === '/orm/post/2table') {
                $this->handle2Table($response);
            } elseif ($path === '/orm/post/3table') {
                $this->handle3Table($response);
            } elseif ($path === '/orm/post/4table') {
                $this->handle4Table($response);
            } else {
                $response->setStatusCode(404);
                $response->end(json_encode(['error' => 'Not found']));
            }
        });

        $http->start();
    }

    private function handle1Table(Response $response) {
        try {
            $randId = bin2hex(random_bytes(4));
            $user = User::create(['name' => "User_{$randId}", 'email' => "test_{$randId}@example.com"]);
            $response->setStatusCode(201);
            $response->end(json_encode(['user_id' => $user->id]));
        } catch (\Exception $e) {
            $response->setStatusCode(500);
            $response->end(json_encode(['error' => $e->getMessage()]));
        }
    }

    private function handle2Table(Response $response) {
        try {
            Capsule::transaction(function() use (&$user) {
                $randId = bin2hex(random_bytes(4));
                $user = User::create(['name' => "User_{$randId}", 'email' => "test_{$randId}@example.com"]);
                Profile::create(['user_id' => $user->id, 'bio' => "Bio for user {$user->id}", 'phone' => "555-{$randId}"]);
            });
            $response->setStatusCode(201);
            $response->end(json_encode(['user_id' => $user->id]));
        } catch (\Exception $e) {
            $response->setStatusCode(500);
            $response->end(json_encode(['error' => $e->getMessage()]));
        }
    }

    private function handle3Table(Response $response) {
        try {
            Capsule::transaction(function() use (&$user) {
                $randId = bin2hex(random_bytes(4));
                $user = User::create(['name' => "User_{$randId}", 'email' => "test_{$randId}@example.com"]);
                Profile::create(['user_id' => $user->id, 'bio' => "Bio for user {$user->id}", 'phone' => "555-{$randId}"]);
                Order::create(['user_id' => $user->id, 'total_amount' => 100.00]);
            });
            $response->setStatusCode(201);
            $response->end(json_encode(['user_id' => $user->id]));
        } catch (\Exception $e) {
            $response->setStatusCode(500);
            $response->end(json_encode(['error' => $e->getMessage()]));
        }
    }

    private function handle4Table(Response $response) {
        try {
            Capsule::transaction(function() use (&$user) {
                $randId = bin2hex(random_bytes(4));
                $user = User::create(['name' => "User_{$randId}", 'email' => "test_{$randId}@example.com"]);
                Profile::create(['user_id' => $user->id, 'bio' => "Bio for user {$user->id}", 'phone' => "555-{$randId}"]);
                $order = Order::create(['user_id' => $user->id, 'total_amount' => 100.00]);
                
                OrderItem::insert([
                    ['order_id' => $order->id, 'product_name' => "Product_{$randId}_1", 'price' => 25.00],
                    ['order_id' => $order->id, 'product_name' => "Product_{$randId}_2", 'price' => 75.00]
                ]);
            });
            $response->setStatusCode(201);
            $response->end(json_encode(['user_id' => $user->id]));
        } catch (\Exception $e) {
            $response->setStatusCode(500);
            $response->end(json_encode(['error' => $e->getMessage()]));
        }
    }
}

$server = new BenchmarkOrmServer();
$server->start();
?>
