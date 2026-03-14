document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const generateBtn = document.getElementById("generateBtn");
    const loadingState = document.getElementById("loading");
    const errorMsg = document.getElementById("errorMsg");
    const resultSection = document.getElementById("resultSection");
    const reportContent = document.getElementById("reportContent");
    const downloadBtn = document.getElementById("downloadBtn");
    
    let currentMarkdown = "";

    // Drag and Drop Logic
    document.querySelectorAll(".file-input").forEach((inputElement) => {
        const dropZone = inputElement.closest(".file-drop-area");

        dropZone.addEventListener("click", (e) => {
            // allows clicking the box to trigger exactly as if input clicked
            // inputElement.click(); 
        });

        inputElement.addEventListener("change", (e) => {
            if (inputElement.files.length) {
                updateFileDisplay(dropZone, inputElement.files[0].name);
            }
        });

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });

        ["dragleave", "dragend"].forEach((type) => {
            dropZone.addEventListener(type, (e) => {
                dropZone.classList.remove("dragover");
            });
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("dragover");

            if (e.dataTransfer.files.length) {
                inputElement.files = e.dataTransfer.files;
                updateFileDisplay(dropZone, e.dataTransfer.files[0].name);
            }
        });
    });

    function updateFileDisplay(dropZone, filename) {
        let msgElement = dropZone.querySelector(".file-msg");
        msgElement.innerHTML = `<strong>Selected:</strong><br>${filename}`;
        dropZone.style.borderColor = "var(--primary)";
        
        // Add a checkmark icon
        let iconElement = dropZone.querySelector(".file-icon");
        iconElement.className = "fa-solid fa-circle-check file-icon";
        iconElement.style.color = "var(--primary)";
    }

    // Form Submission Logic
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(uploadForm);

        // UI States
        generateBtn.classList.add("hidden");
        loadingState.classList.remove("hidden");
        errorMsg.classList.add("hidden");
        resultSection.classList.add("hidden");

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Failed to generate report");
            }

            // Success: Render Markdown
            currentMarkdown = data.markdown;
            
            // marked.js options to help cleanly render raw text
            marked.setOptions({
                breaks: true,
                gfm: true
            });
            
            reportContent.innerHTML = marked.parse(currentMarkdown);
            
            // Show results UI
            resultSection.classList.remove("hidden");
            
            // Scroll to results smoothly
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            errorMsg.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}`;
            errorMsg.classList.remove("hidden");
        } finally {
            // Reset Button States
            loadingState.classList.add("hidden");
            generateBtn.classList.remove("hidden");
        }
    });

    // Download Markdown Logic
    downloadBtn.addEventListener("click", () => {
        if (!currentMarkdown) return;
        
        const blob = new Blob([currentMarkdown], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "DDR_Report.md";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
