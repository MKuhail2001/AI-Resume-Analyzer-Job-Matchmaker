// Initialize AOS for animation on scroll
AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true,
  });
  
  // Load and render analysis result from localStorage (mock)
  const result = localStorage.getItem("resumeAnalysis");
  
  if (result) {
    const parsed = parseResult(result); // JSON.parse if needed
  
    // Populate Resume Summary
    document.getElementById("summaryText").innerText =
      parsed.summary || "No summary provided.";
  
    // Populate Score Badge
    if (parsed.score !== undefined) {
      const scoreBadge = document.getElementById("scoreBadge");
      scoreBadge.innerText = `${parsed.score} / 100`;
  
      // Set badge color based on score
      if (parsed.score >= 80) {
        scoreBadge.className = "badge bg-success score-badge";
      } else if (parsed.score >= 50) {
        scoreBadge.className = "badge bg-warning text-dark score-badge";
      } else {
        scoreBadge.className = "badge bg-danger score-badge";
      }
    }
  
    // Populate Fit Text
    document.getElementById("fitText").innerText =
      parsed.fit || "Fit information not available.";
  
  } else {
    alert("⚠️ No resume analysis result found. Please upload a resume first.");
  }
  
  // Parse function (customize if your analysis is in JSON format)
  function parseResult(text) {
    try {
      return JSON.parse(text); // If JSON string
    } catch (e) {
      return { summary: text }; // If plain string fallback
    }
  }
  
  // Handle Generate Resume button
  document.getElementById("generateBtn").addEventListener("click", function () {
    const button = this;
    const originalText = button.innerHTML;
  
    button.disabled = true;
    button.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
  
    setTimeout(() => {
      document.getElementById("downloadSection").style.display = "block";
      button.disabled = false;
      button.innerHTML = originalText;
  
      document.getElementById("downloadSection").scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 2000);
  });
  
  // Download mock
  document.getElementById("downloadBtn").addEventListener("click", function (e) {
    e.preventDefault();
    alert("✅ Your improved resume has been downloaded!");
  });
  
