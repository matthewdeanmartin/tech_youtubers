Title: Other YouTubers
Date: 2026-06-20
Slug: other
sortorder: 18
Summary: Other YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (1)</h2>

<ul>
<li data-lang="en"><strong><a href="https://www.youtube.com/channel/UC8XOX31MAHVCHKSMKCj8oDg" target="_blank" rel="noopener noreferrer">YouTuber</a></strong> · <a href="https://upvo.me/author/youtuber/" target="_blank" rel="noopener noreferrer">Mastodon</a> — SUBSCRIBE TO MY YOUTUBE CHANNEL<button type="button" class="creator-follow" data-mastodon-acct="author/youtuber@upvo.me" hidden>Follow on Mastodon</button><div class="recent-videos"><p class="recent-videos__title">Recent uploads (5)</p><ul><li><time datetime="2026-05-28">2026-05-28</time> · <a href="https://www.youtube.com/shorts/m3hTXOpAsS8" target="_blank" rel="noopener noreferrer">Papa VS #AI</a></li><li><time datetime="2026-05-27">2026-05-27</time> · <a href="https://www.youtube.com/watch?v=UAN-9meJdUU" target="_blank" rel="noopener noreferrer">Zašto web sajtovi UMIRU u 2026</a></li><li><time datetime="2026-05-08">2026-05-08</time> · <a href="https://www.youtube.com/shorts/yDH5yHVnaRs" target="_blank" rel="noopener noreferrer">Zašto je YouTube budućnost za #digitalnimarketing</a></li><li><time datetime="2026-05-06">2026-05-06</time> · <a href="https://www.youtube.com/shorts/T76DwDbNsT8" target="_blank" rel="noopener noreferrer">Digitalni Marketing Kurs  #digitalnimarketing</a></li><li><time datetime="2026-05-05">2026-05-05</time> · <a href="https://www.youtube.com/shorts/HDK4FCMrnuc" target="_blank" rel="noopener noreferrer">Unaprijedi onlajn prodaju</a></li></ul></div></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="other" data-bulk-handles="[&quot;@author/youtuber@upvo.me&quot;]">
<h2>Follow this account</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-other">Native accounts in Other</label>
<textarea id="bulk-follow-other" class="bulk-follow__text" rows="6" readonly spellcheck="false">@author/youtuber@upvo.me</textarea>
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

