import argparse
from persons_data_etl.etl import ETL


def main():
    parser = argparse.ArgumentParser(description='Run FakerAPI persons data ETL')
    parser.add_argument('--data_size', metavar='path', help="Total size of data to fetch, Default = 1000", required=False)
    parser.add_argument('--batch_size', metavar='path', help="Data batch size to fetch per iteration, Default = 100", required=False)
    parser.add_argument('--delay', metavar='path', help="Time to wait till the next run or try, Default = 5 seconds", required=False)
    parser.add_argument('--retries', metavar='path', help="Number of attempts, Default = 5", required=False)
    parser.add_argument('--logging', metavar='path', help="Display ETL logs to console, Default = True", required=False)

    args = parser.parse_args()
    data_size = int(args.data_size) if args.data_size else 1000
    batch_size = int(args.batch_size) if args.batch_size else 100
    delay_time = int(args.delay) if args.delay else 5
    num_of_retries = int(args.retries) if args.retries else 5
    with_logging = bool(args.logging) if args.logging else True

    etl_instance = ETL()
    etl_instance.run(data_size, batch_size, num_of_retries, delay_time, with_logging)


if __name__ == '__main__':
    main()