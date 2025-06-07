import mimetypes
import hashlib
from urllib.parse import urlparse
from django.conf import settings
from supabase import create_client

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_image(file, folder=None):
    """
    Uploads an image to Supabase storage and returns (success, result).
    If success is True, result is the public URL.
    If success is False, result is the error message.
    """
    try:
        if folder is None:
            folder = 'uploads'
        # File validation
        allowed_extensions = ['jpg', 'jpeg', 'png']
        max_size = 4 * 1024 * 1024  # 4 MB
        file_extension = file.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            return False, ('client', "Unsupported file extension. Only JPG, JPEG, and PNG are allowed.")

        if file.size > max_size:
            return False, ('client', "File too large. Maximum size allowed is 4MB.")

        # Read file and generate MD5 hash
        file.seek(0)
        file_content = file.read()
        file_hash = hashlib.md5(file_content).hexdigest()

        # Create unique filename and path
        unique_filename = f"{file_hash}.{file_extension}"
        file_path = f"{folder}/{unique_filename}"

        # Guess MIME type
        mime_type, _ = mimetypes.guess_type(file.name)
        if mime_type is None:
            return False, ('client', "Unsupported file type.")

        # Upload to Supabase
        response = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            file_path,
            file_content,
            {'content-type': mime_type}
        )

        # Check upload result
        if isinstance(response, dict) and 'error' in response:
            return False, ('server', response['error']['message'])

        # Build public URL
        public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{file_path}"
        return True, public_url

    except Exception as e:
        return False, ('server', str(e))

def delete_image(image_url):
    try:
        parsed = urlparse(image_url)
        path = parsed.path.lstrip('/')
        bucket_name = settings.SUPABASE_BUCKET
        expected_prefix = f"storage/v1/object/public/{bucket_name}/"
        
        if not path.startwith(expected_prefix):
            return False, "Invalid image URL format."
        relative_path = path[len(expected_prefix):]
        response = supabase.storage.from_(bucket_name).remove([relative_path])
        if isinstance(response, dict) and 'error' in response:
            return False, response['error']['message']
        if response.get('data') and len(response['data']) > 0: 
            return True, "Image deleted successfully."
        return False, "Image not found or already deleted."
    except Exception as e:
        return False, str(e)