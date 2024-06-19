from PIL import Image
import requests
from io import BytesIO

def download_image(url, headers=None):
    response = requests.get(url, headers=headers)
    return Image.open(BytesIO(response.content))

def get_piece_coordinates(image):
    # This function assumes the pieces are arranged in a 2x6 grid in the image
    # Adjust the coordinates based on the specific layout of your image
    piece_coordinates = [
        (0, 0), (100, 0), (200, 0), (300, 0), (400, 0), (500, 0),
        (0, 100), (100, 100), (200, 100), (300, 100), (400, 100), (500, 100)
    ]
    return piece_coordinates

def split_chess_pieces(image, output_folder, piece_size=100):
    piece_coordinates = get_piece_coordinates(image)

    # Create and save individual chess piece images
    for idx, (x, y) in enumerate(piece_coordinates):
        x_centered = x + (piece_size - image.width % piece_size) // 2
        y_centered = y + (piece_size - image.height % piece_size) // 2

        piece_image = image.crop((x_centered, y_centered, x_centered + piece_size, y_centered + piece_size))
        piece_image.save(f"{output_folder}/piece_{idx + 1}.png")

if __name__ == "__main__":
    chess_pieces_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Chess_Pieces_Sprite.svg/640px-Chess_Pieces_Sprite.svg.png"
    output_folder_path = "images"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    chess_pieces_image = download_image(chess_pieces_image_url, headers=headers)
    split_chess_pieces(chess_pieces_image, output_folder_path, piece_size=100)
