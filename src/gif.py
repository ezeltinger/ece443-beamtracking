import imageio
import os
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def create_gif(name):
    OUTPUT_PATH = os.path.relpath('..\\output')
    files = [os.path.join(OUTPUT_PATH, f) for f in os.listdir(OUTPUT_PATH) if os.path.isfile(os.path.join(OUTPUT_PATH, f))]

    # Build GIF
    files.sort(key=natural_keys)
    if files:
        with imageio.get_writer(f'{OUTPUT_PATH}/{name}.gif', mode='I') as writer:
            for file in files:
                if file.endswith('.png'):
                    image = imageio.imread(file)
                    writer.append_data(image)
            # Pause on the last frame
            for _ in range(5):
                image = imageio.imread(files[-1])
                writer.append_data(image)
    
        # Remove files
        for file in set(files):
            try:
                if file.endswith('.png'):
                    os.remove(file)
            except OSError:
                pass
