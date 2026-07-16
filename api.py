import requests

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    headers = {
        'User-Agent': 'InventoryApp - Flask - Student Project' 
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status Code:", response.status_code) 
        print("Raw Response:", response.text[:200])  
        
        if response.status_code != 200:
            return None

        data = response.json()

        if data.get('status') == 1:  
            product = data['product']
            return {
                "barcode": barcode,
                "name": product.get('product_name', 'Unknown'),
                "brand": product.get('brands', 'Unknown'),
                "description": product.get('generic_name', ''),
                "image": product.get('image_front_url', '')
            }
        else:
            return None 
            
    except requests.exceptions.RequestException as e:
        print("Network Error:", e)
        return None
    except ValueError as e:  
        print("JSON Error:", e)
        return None


if __name__ == "__main__":
    result = get_product_by_barcode("3017620422003")  
    print(result)