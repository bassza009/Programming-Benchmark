hyperfine --warmup 3 --runs 20 --export-json php.dkr.json \
 'docker exec phpbench php -d opcache.enable_cli=0 prisoners.php'
