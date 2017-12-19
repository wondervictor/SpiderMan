# -*- coding: utf-8 -*-
import argparse

from parallel import worker
from crawler import login, geturl

AUTH_KEY = "dasfbq3G^%ERFSTYIVI*&R^F &#^C"


def main(opt):

    if opt.master:
        # start as master node
        node = worker.Master(address=("0.0.0.0", opt.port), authkey=AUTH_KEY)
        node.start()

    else:
        # start as worker node
        config = worker.WorkerConfig(
            name='worker',
            task_batchsize=4,
            crawler_threads=2,
            parser_threads=4,
            authkey=AUTH_KEY,
            address=(opt.master_ip, opt.port)
        )
        login_manager = login.Login()
        login_manager.check()

        def parse():
            pass

        node = worker.Worker(config=config, crawler_func=geturl.get_html, parser_func=parse)
        node.login_manager = login_manager
        node.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--master', type=bool, default=False, help='Master Node')
    parser.add_argument('--port', type=int, default=2333, help='Master node port')
    parser.add_argument('--master_ip', type=str, default="127.0.0.1", help='Master node IP')

    args = parser.parse_args()
    main(args)