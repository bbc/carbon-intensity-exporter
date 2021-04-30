from carbon_minimiser.api.app import app
import argparse


def main(port):
    app.run(port=port)


parser = argparse.ArgumentParser()
parser.add_argument('-p')
args = parser.parse_args()
if args.p:
    port = int(args.p)
else:
    port = 8080

main(port)
