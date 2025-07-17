 # Adobe Hackathon Round 1A

## How to Run

1. Put PDF files into the `input` folder
2. Build the image:
   ```bash
   docker build --platform linux/amd64 -t adobe-1a .
3. Run the container:
   ```powershell
   docker run --rm -v ${PWD}\input:/app/input -v ${PWD}\output:/app/output --network none adobe-1a
4. Output json files can be seen from the `output` folder
