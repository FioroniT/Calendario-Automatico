
      async function readFile(file) {
        try {
          const response = await fetch(file);

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const text = await response.text();
          return text;
        } catch (error) {
          console.error("Could not read the file!", error);
          return null;
        }
      }
      const items = await readFile('carreras.txt');
      const dropdowncontent = document.getelementbyid("dpdw-carreras");
      items.forEach(item => {
        const button = document.createElement("button");
        button.textContent = item;
        button.addEventListener("click", function() {
          document.getElementById("carreras-btn").innerText = item;
        });
        dropdownContent.appendChild(button);
      })
