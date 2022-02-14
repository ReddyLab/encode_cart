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


def create_cart(url, auth, cart_name):
    request_body = {"name": cart_name}
    create_response = requests.put(url, json=request_body, auth=auth)
    create_json = create_response.json()

    if create_json["status"] != "success":
        raise Exception(f"Create cart request failed: {create_json}")

    return create_json


def add_to_cart(url, auth, accession_ids, cart_name):
    request_body = {"elements": accession_ids, "name": cart_name}
    put_response = requests.put(url, json=request_body, auth=auth)
    put_response_json = put_response.json()

    if put_response_json["status"] != "success":
        raise Exception(f"Add items to cart failed: {put_response_json}")

    return put_response_json


def main(test, auth_file, accession_file, cart_name):
    base_url = TEST_URL if test else PROD_URL

    auth = load_auth(auth_file)

    try:
        create_response_json = create_cart(create_url(base_url), auth, cart_name)
    except Exception as e:
        raise e

    try:
        cart_id = create_response_json["@graph"][0]
    except:
        raise Exception(f"malformed json: {create_response_json}")

    accession_ids = load_accessions(accession_file)

    try:
        put_response_json = add_to_cart(
            cart_url(base_url, cart_id), auth, accession_ids, cart_name
        )
    except Exception as e:
        raise e

    return cart_id, put_response_json


def parse_args():
    parser = argparse.ArgumentParser("encode_carts")
    parser.add_argument("-n", "--name", type=str, required=True)
    parser.add_argument("-f", "--authfile", type=argparse.FileType(), required=True)
    parser.add_argument("-a", "--accessions", type=argparse.FileType(), required=True)
    parser.add_argument("-t", "--test", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        cart_id, add__to_cart_json = main(
            args.test, args.authfile, args.accessions, args.name
        )
    except Exception as e:
        print(e)
        exit(1)

    print(f"Cart id: {cart_id}")
    print(f"Items Added to Cart:\n{add__to_cart_json}")
