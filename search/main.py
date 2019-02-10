import argparse
import status, index_manager, update

def main():
    parser = argparse.ArgumentParser(prog='searchtool', description="Index a file tree and search it.")
    parser.add_argument('--path', help='Index path', default='.')

    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init', help='Init index')
    init_parser.set_defaults(func=init_index)

    status_parser = subparsers.add_parser('status', help='Status of index')
    status_parser.set_defaults(func=get_status)

    update_parser = subparsers.add_parser('update', help='Update index')
    update_parser.add_argument('--delete-missing', dest='delete_missing', help='Delete files that no longer exist', action='store_true')
    update_parser.set_defaults(func=update_index)

    query_parser = subparsers.add_parser('query', aliases=['q'], help='Query index')
    query_parser.set_defaults(func=run_query)
    query_parser.add_argument('terms', metavar='term',
                              type=str, nargs='+', help='Search query terms')

    args = parser.parse_args()
    if 'func' not in args:
        # we fell through all the subparsers
        parser.print_help()
        return
    args.func(args)

def init_index(args):
    index_manager.create_index(args.path)
    print("Index created")

def get_status(args):
    print(status.format_status(status.status(args.path)))

def update_index(args):
    work_plan = status.status(args.path)
    formatted_status = status.format_status(work_plan)
    update.update(args.path, work_plan, delete=args.delete_missing)
    if formatted_status == '':
        print('No changes.')
        return
    print(formatted_status)
    if args.delete_missing:
        print('Missing objects removed from index.')
    else:
        print('Missing objects NOT removed from index.')

def run_query(args):
    print('query: %s' % ' '.join(args.terms))

if __name__ == '__main__':
    main()