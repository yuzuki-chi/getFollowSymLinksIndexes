# getFollowSymLinksIndexes

このスクリプトは, Apacheサーバの一定条件にあたる場合に使用可能.

`/etc/httpd/conf/httpd.conf`
```
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
</Directory>
```

`Options Indexes FollowSymLinks`

となっている場合. つまり, FollowSymLinksが有効になっている場合に使用できる. 

`main.py` にて, 取得先(url)と出力先(output_dir)を指定する. 
```
url: str = "https://sample.com/"
output_dir: str = "sample.com"
```

初期値は sample.com となっているが, FollowSymLinks の機能が有効かつ, ファイル一覧が表示されるページである必要がある. 

実は, FollowSymLinks が向こうの場合でも, htmlファイルを取得して, aタグで指定されたリンクを再帰的に取得し続けることが可能. 
WordPressにアップロードされている画像を収集することを目的としているため, 様々なフィルターがかけられ最適化されている. 
今後, オプションとしてユースケースごとに最適化された動きをするように変更を加えていく予定.
