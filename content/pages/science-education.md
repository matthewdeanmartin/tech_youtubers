Title: Science & Education YouTubers
Date: 2026-06-20
Slug: science-education
sortorder: 12
Summary: Science & Education YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (2)</h2>

<ul>
<li data-lang="en"><strong><a href="https://www.youtube.com/@InsiderPhD" target="_blank" rel="noopener noreferrer">InsiderPhD</a></strong> · <a href="https://infosec.exchange/@insiderphd" target="_blank" rel="noopener noreferrer">Mastodon</a> — Application security, API security, bug bounty hunting, and practical security research education.<button type="button" class="creator-follow" data-mastodon-acct="insiderphd@infosec.exchange" hidden>Follow on Mastodon</button><div class="recent-videos"><p class="recent-videos__title">Recent uploads (5)</p><ul><li><time datetime="2026-01-16">2026-01-16</time> · <a href="https://www.youtube.com/watch?v=yMoq17-1pJA" target="_blank" rel="noopener noreferrer">I bought this tiny $40 ereader… Then rewrote It</a></li><li><time datetime="2025-08-13">2025-08-13</time> · <a href="https://www.youtube.com/watch?v=CpV3XDqzYyE" target="_blank" rel="noopener noreferrer">Analysing the DOM to find Reflected XSS</a></li><li><time datetime="2025-07-31">2025-07-31</time> · <a href="https://www.youtube.com/watch?v=8Uva1su3goc" target="_blank" rel="noopener noreferrer">Still not found your first bug? Try IDORs</a></li><li><time datetime="2025-05-29">2025-05-29</time> · <a href="https://www.youtube.com/watch?v=wnVpmSrhNRo" target="_blank" rel="noopener noreferrer">Vibe Coding in Cursor for Cyber Security</a></li><li><time datetime="2025-04-15">2025-04-15</time> · <a href="https://www.youtube.com/shorts/KIgaZb_IjHU" target="_blank" rel="noopener noreferrer">I designed and built eink labels for my filament with an ESP32, here’s how it works #3dprinting</a></li></ul></div></li>
<li data-lang="en"><strong><a href="https://www.youtube.com/channel/UC90iyXKrUsJBCYbtdbgrmkg" target="_blank" rel="noopener noreferrer">Open Latin</a></strong> · <a href="https://colloquium.social/@lingualatina" target="_blank" rel="noopener noreferrer">Mastodon</a> — Help us create Open Latin resources # Classics # LinguaLatina # latin ? # latineloquor # salvete<button type="button" class="creator-follow" data-mastodon-acct="lingualatina@colloquium.social" hidden>Follow on Mastodon</button><div class="recent-videos"><p class="recent-videos__title">Recent uploads (5)</p><ul><li><time datetime="2022-04-04">2022-04-04</time> · <a href="https://www.youtube.com/watch?v=7ILCZqbPaJw" target="_blank" rel="noopener noreferrer">Catalhoyuk</a></li><li><time datetime="2022-01-02">2022-01-02</time> · <a href="https://www.youtube.com/watch?v=ZIBDtl3-bCw" target="_blank" rel="noopener noreferrer">Urbs Hierosolyma</a></li><li><time datetime="2021-10-19">2021-10-19</time> · <a href="https://www.youtube.com/watch?v=dNIerNvnCos" target="_blank" rel="noopener noreferrer">Limes Germanicus et Vallum Aelium</a></li><li><time datetime="2021-10-14">2021-10-14</time> · <a href="https://www.youtube.com/watch?v=v2sUh0X14Io" target="_blank" rel="noopener noreferrer">Angkor</a></li><li><time datetime="2021-10-12">2021-10-12</time> · <a href="https://www.youtube.com/watch?v=pdAm0qODjTc" target="_blank" rel="noopener noreferrer">Vita Romae</a></li></ul></div></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="science-education" data-bulk-handles="[&quot;@insiderphd@infosec.exchange&quot;, &quot;@lingualatina@colloquium.social&quot;]">
<h2>Follow these 2 accounts</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-science-education">Native accounts in Science &amp; Education</label>
<textarea id="bulk-follow-science-education" class="bulk-follow__text" rows="6" readonly spellcheck="false">@insiderphd@infosec.exchange
@lingualatina@colloquium.social</textarea>
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

