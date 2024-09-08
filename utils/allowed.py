'''
validates file extension before uploading
'''

def allowed_file(filename):
    '''
    Validates the extension 
    Returns True if valid and False if otherwise
    '''
    
    allowed_extensions = ['png', 'jpeg', 'gif', 'webp', 'jpg']

    if '.' in filename:
        '''
        checks if the filename has an extension
        '''
        # split the file once from the right using the . as a benchmark
        parts = filename.rsplit('.', 1)
        
        # extract the extension and convert it to lower case
        extension = parts[1].lower()

        # check if the extension is in the list of valid extensions
        if extension in allowed_extensions:
            return True
        else:
            return False
    else:
        return False
