Title: Culture & Entertainment YouTubers
Date: 2026-06-20
Slug: culture-entertainment
sortorder: 16
Summary: Culture & Entertainment YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (1)</h2>

<ul>
<li data-lang="en"><strong><a href="https://www.youtube.com/c/techhuthd" target="_blank" rel="noopener noreferrer">TechHut</a></strong> · <a href="https://fosstodon.org/@techhut" target="_blank" rel="noopener noreferrer">Mastodon</a> — Yes, I use this account and check it out frequently. No, you don&#x27;t need to tag an admin to try to get me in trouble. TechHut Media.<button type="button" class="creator-follow" data-mastodon-acct="techhut@fosstodon.org" hidden>Follow on Mastodon</button><div class="recent-videos"><p class="recent-videos__title">Recent uploads (5)</p><ul><li><time datetime="2024-05-22">2024-05-22</time> · <a href="https://www.youtube.com/watch?v=1yrChg7XW-A" target="_blank" rel="noopener noreferrer">Share folders with other computers! Network Shares on Windows Guide</a></li><li><time datetime="2024-05-22">2024-05-22</time> · <a href="https://www.youtube.com/watch?v=Ipnnt6f7d4I" target="_blank" rel="noopener noreferrer">RAID in Windows? How to a Create Storage Pool</a></li><li><time datetime="2024-05-22">2024-05-22</time> · <a href="https://www.youtube.com/watch?v=9kQ75FxxkUw" target="_blank" rel="noopener noreferrer">How to Enable OpenSSH and SFTP in Windows</a></li><li><time datetime="2024-05-22">2024-05-22</time> · <a href="https://www.youtube.com/watch?v=vzxu9Vn6tJs" target="_blank" rel="noopener noreferrer">How to Enable Remote Desktop in Windows 11</a></li><li><time datetime="2024-05-22">2024-05-22</time> · <a href="https://www.youtube.com/watch?v=lTlGJC6irNQ" target="_blank" rel="noopener noreferrer">the BEST way to install Windows 11</a></li></ul></div></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="culture-entertainment" data-bulk-handles="[&quot;@techhut@fosstodon.org&quot;]">
<h2>Follow this account</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-culture-entertainment">Native accounts in Culture &amp; Entertainment</label>
<textarea id="bulk-follow-culture-entertainment" class="bulk-follow__text" rows="6" readonly spellcheck="false">@techhut@fosstodon.org</textarea>
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

