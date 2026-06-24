Title: Gaming & VTubers YouTubers
Date: 2026-06-20
Slug: gaming
sortorder: 11
Summary: Gaming & VTubers YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (1)</h2>

<ul>
<li data-lang="en"><strong><a href="https://www.youtube.com/gregandcin" target="_blank" rel="noopener noreferrer">gregandcin</a></strong> · <a href="https://mindly.social/@gregandcin" target="_blank" rel="noopener noreferrer">Mastodon</a> — I kinda like games and tech. Local connoAsseur. Rested and Sleeppilled. Admin #2 of Mindly.Social # fedi22 # tech # gaming # anime # manga # keyboards<button type="button" class="creator-follow" data-mastodon-acct="gregandcin@mindly.social" hidden>Follow on Mastodon</button><div class="recent-videos"><p class="recent-videos__title">Recent uploads (5)</p><ul><li><time datetime="2017-06-23">2017-06-23</time> · <a href="https://www.youtube.com/watch?v=dcksMdWlmXA" target="_blank" rel="noopener noreferrer">I&#x27;M NOT EVEN MAD</a></li><li><time datetime="2017-05-26">2017-05-26</time> · <a href="https://www.youtube.com/watch?v=2op2CCg1xZ0" target="_blank" rel="noopener noreferrer">I just bought this - Overwatch Livestream May 22, 2017</a></li><li><time datetime="2017-05-26">2017-05-26</time> · <a href="https://www.youtube.com/watch?v=Q8u8lGMQx8E" target="_blank" rel="noopener noreferrer">1v1 Scrub - Overwatch Livestream May 23, 2017</a></li><li><time datetime="2017-05-26">2017-05-26</time> · <a href="https://www.youtube.com/watch?v=ULaOkdACeWQ" target="_blank" rel="noopener noreferrer">NEW OPERATION GUYS - CS:GO Livestream May 23, 2017</a></li><li><time datetime="2017-05-25">2017-05-25</time> · <a href="https://www.youtube.com/watch?v=LAEMjzC4HtU" target="_blank" rel="noopener noreferrer">gregandcin Live Live Stream</a></li></ul></div></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="gaming" data-bulk-handles="[&quot;@gregandcin@mindly.social&quot;]">
<h2>Follow this account</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-gaming">Native accounts in Gaming &amp; VTubers</label>
<textarea id="bulk-follow-gaming" class="bulk-follow__text" rows="6" readonly spellcheck="false">@gregandcin@mindly.social</textarea>
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

