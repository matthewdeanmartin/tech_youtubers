Title: Art, Design & Making YouTubers
Date: 2026-06-20
Slug: art-making
sortorder: 14
Summary: Art, Design & Making YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (1)</h2>

<ul>
<li data-lang="en"><strong><a href="https://www.youtube.com/@undecidedtechnology" target="_blank" rel="noopener noreferrer">Matt Ferrell / Undecided</a></strong> · <a href="https://mastodon.social/@mattferrell" target="_blank" rel="noopener noreferrer">Mastodon</a> — Clean tech, energy, and future technology explained clearly. Covers EVs, solar, wind, and emerging sustainable tech.<details class="recent-videos"><summary>Recent uploads (5)</summary><ul><li><time datetime="2026-06-10">2026-06-10</time> · <a href="https://www.youtube.com/watch?v=XbnuBbvX5_U" target="_blank" rel="noopener noreferrer">306: Is This Finally a Real Solid State Battery? With Jorge Diaz Scheider</a></li><li><time datetime="2026-05-27">2026-05-27</time> · <a href="https://www.youtube.com/watch?v=0bw2IU73RG4" target="_blank" rel="noopener noreferrer">305: Having a Think with Dave Borlace</a></li><li><time datetime="2026-05-13">2026-05-13</time> · <a href="https://www.youtube.com/watch?v=quA0gBAFEQk" target="_blank" rel="noopener noreferrer">304: JerryRigged Wheelchairs and More with Zack Nelson</a></li><li><time datetime="2026-04-29">2026-04-29</time> · <a href="https://www.youtube.com/watch?v=gfCZL-vwWtA" target="_blank" rel="noopener noreferrer">303: Karl Rábago and the Internet of Electricity</a></li><li><time datetime="2026-04-15">2026-04-15</time> · <a href="https://www.youtube.com/watch?v=nR8qn3cD1jQ" target="_blank" rel="noopener noreferrer">302: The Future of Food with Nona Yehia</a></li></ul></details></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="art-making" data-bulk-handles="[&quot;@mattferrell@mastodon.social&quot;]">
<h2>Follow this account</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-art-making">Native accounts in Art, Design &amp; Making</label>
<textarea id="bulk-follow-art-making" class="bulk-follow__text" rows="6" readonly spellcheck="false">@mattferrell@mastodon.social</textarea>
<div class="bulk-follow__actions">
<button type="button" class="bulk-follow__copy" data-bulk-copy>Copy handles</button>
<a class="bulk-follow__download" data-bulk-download href="#" download>Download CSV</a>
</div>
</section>

<script>
(function () {
  function csvFor(handles) {
    var rows = ["Account address,Show boosts,Notify on new posts,Languages"];
    handles.forEach(function (h) { rows.push(h.replace(/^@/, "") + ",true,false,"); });
    return rows.join("\n") + "\n";
  }
  function stamp() {
    var d = new Date();
    function p(n) { return String(n).padStart(2, "0"); }
    return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + "-" +
           p(d.getHours()) + p(d.getMinutes()) + p(d.getSeconds());
  }
  document.querySelectorAll(".bulk-follow").forEach(function (section) {
    var handles;
    try { handles = JSON.parse(section.getAttribute("data-bulk-handles")) || []; }
    catch (e) { handles = []; }
    var scope = section.getAttribute("data-bulk-scope") || "accounts";

    var copyBtn = section.querySelector("[data-bulk-copy]");
    var textarea = section.querySelector(".bulk-follow__text");
    if (copyBtn && textarea) {
      copyBtn.addEventListener("click", function () {
        var text = handles.join("\n");
        function done() {
          var original = copyBtn.textContent;
          copyBtn.textContent = "Copied!";
          setTimeout(function () { copyBtn.textContent = original; }, 1500);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () {
            textarea.select(); document.execCommand("copy"); done();
          });
        } else {
          textarea.select(); document.execCommand("copy"); done();
        }
      });
    }

    var dl = section.querySelector("[data-bulk-download]");
    if (dl) {
      dl.addEventListener("click", function (e) {
        e.preventDefault();
        var blob = new Blob([csvFor(handles)], { type: "text/csv;charset=utf-8" });
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        // Unique per scope and per download so saved files never collide.
        a.download = "mastodon-follows-" + scope + "-" + stamp() + ".csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 0);
      });
    }
  });
})();
</script>

