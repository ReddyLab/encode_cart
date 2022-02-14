import argparse
import requests


TEST_URL = "https://test.encodedcc.org"
PROD_URL = "https://www.encodeproject.org"


def load_auth(auth_file) -> tuple[str, str]:
    line = auth_file.readline().strip().split()
    return (line[0], line[1])


def create_url(base_url) -> str:
    return f"{base_url}/carts/@@put-cart"


def cart_url(base_url, cart_id) -> str:
    return f"{base_url}{cart_id}"


def load_accessions(accesion_file) -> list[str]:
    return [accession_id.strip() for accession_id in accesion_file]


def main(test, auth_file, accession_file, cart_name):
    base_url = TEST_URL if test else PROD_URL
    create_json = {"name": cart_name}
    auth = load_auth(auth_file)

    try:
        create_response = requests.put(
            create_url(base_url), json=create_json, auth=auth
        )
        create_json = create_response.json()
    except Exception as e:
        print(e)
        exit(1)

    if create_json["status"] != "success":
        print(f"Create cart request failed: {create_json}")

    try:
        cart_id = create_json["@graph"][0]
    except:
        print(f"malformed json: {create_json}")
        exit(1)

    print(f"cart id: {cart_id}")

    accession_ids = load_accessions(accession_file)

    put_request_json = {"elements": accession_ids, "name": cart_name}
    try:
        put_response = requests.put(
            cart_url(base_url, cart_id), json=put_request_json, auth=auth
        )
        put_response_json = put_response.json()
    except Exception as e:
        print(e)
        exit(1)

    if put_response_json["status"] != "success":
        print(f"Add items to cart request failed: {put_response_json}")
        exit(1)

    print(f"Items Added to Cart:\n{put_response_json}")


def parse_args():
    parser = argparse.ArgumentParser("encode_carts")
    parser.add_argument("-n", "--name", type=str, required=True)
    parser.add_argument("-f", "--authfile", type=argparse.FileType(), required=True)
    parser.add_argument("-a", "--accessions", type=argparse.FileType(), required=True)
    parser.add_argument("-t", "--test", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.test, args.authfile, args.accessions, args.name)
