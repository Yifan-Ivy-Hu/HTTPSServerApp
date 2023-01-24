
"""Views, one for each kypair page. source: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html"""
from kvpair.views.index import show_index, get_all, insert_kvpair, delete_kvpair, delete_all_kvpairs, get_value
from kvpair.views.fileupload import get_list, upload_file, download_file