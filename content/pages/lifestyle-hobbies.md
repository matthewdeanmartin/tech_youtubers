Title: Lifestyle, Travel & Hobbies YouTubers
Date: 2026-06-20
Slug: lifestyle-hobbies
sortorder: 17
Summary: Lifestyle, Travel & Hobbies YouTube creators and channel feeds on Mastodon.

<div data-lang-section="native">
<h2>Native Mastodon accounts (5)</h2>

<ul>
<li data-lang="en"><strong><a href="{filename}creator/christophe-grebert.md">Christophe Grébert</a></strong> · <a href="https://www.youtube.com/channel/UC80C0zG_5SgIqLXIfyi9ehg" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://mastodon.top/@grebert" target="_blank" rel="noopener noreferrer">Mastodon</a> — # Vélotafeur à # Paris et banlieue. Mes intérêts : # vélo # mobilité # ville # urbanisme # planète # climat # environnement # démocratie # citoyenneté # médias # LGBT + # plantesvertes<p class="creator-follow-line"><button type="button" class="creator-follow" data-mastodon-acct="grebert@mastodon.top" hidden>Follow on Mastodon</button></p></li>
<li data-lang="en"><strong><a href="{filename}creator/copernicusecmwf.md">CopernicusECMWF</a></strong> · <a href="https://www.youtube.com/channel/UCdK5sfMQcJ64q8AGR_7-ZRw" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://masto.ai/@CopernicusECMWF" target="_blank" rel="noopener noreferrer">Mastodon</a> — The # CopernicusClimate Change Service (#C3S) &amp; # CopernicusAtmosphere Monitoring Service (CAMS), implemented by ECMWF on behalf of the European Commission.<p class="creator-follow-line"><button type="button" class="creator-follow" data-mastodon-acct="CopernicusECMWF@masto.ai" hidden>Follow on Mastodon</button></p></li>
<li data-lang="en"><strong><a href="{filename}creator/ecosia.md">Ecosia</a></strong> · <a href="https://www.youtube.com/channel/UC1_up347GdfKBDVGqwjt7Aw" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://mastodon.social/@ecosia" target="_blank" rel="noopener noreferrer">Mastodon</a> — Find what you need. Plant trees where they’re needed. Search with Ecosia and be climate active every day: <a href="http://ecosia.co/learnmore" target="_blank" rel="noopener noreferrer">http://ecosia.co/learnmore</a><p class="creator-follow-line"><button type="button" class="creator-follow" data-mastodon-acct="ecosia@mastodon.social" hidden>Follow on Mastodon</button></p></li>
<li data-lang="en"><strong><a href="{filename}creator/extinction-rebellion-global.md">Extinction Rebellion Global</a></strong> · <a href="https://www.youtube.com/channel/UCYThdLKE6TDwBJh-qDC6ICA" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://social.rebellion.global/@ExtinctionR" target="_blank" rel="noopener noreferrer">Mastodon</a> — Global non-violent direct action movement demanding a response to the climate and ecological emergency. Donate at bit.ly/supportxr<p class="creator-follow-line"><button type="button" class="creator-follow" data-mastodon-acct="ExtinctionR@social.rebellion.global" hidden>Follow on Mastodon</button></p></li>
<li data-lang="en"><strong><a href="{filename}creator/public-transport-users-assoc.md">Public Transport Users Assoc</a></strong> · <a href="https://www.youtube.com/channel/UCvN7tPwWzZgeKc2jHoN5vew" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://mastodon.social/@ptua" target="_blank" rel="noopener noreferrer">Mastodon</a> — Public Transport Users Association - campaigning for better public transport in Melbourne and around Victoria, Australia<p class="creator-follow-line"><button type="button" class="creator-follow" data-mastodon-acct="ptua@mastodon.social" hidden>Follow on Mastodon</button></p></li>
</ul>
</div>

<section class="bulk-follow" data-bulk-scope="lifestyle-hobbies" data-bulk-handles="[&quot;@grebert@mastodon.top&quot;, &quot;@CopernicusECMWF@masto.ai&quot;, &quot;@ecosia@mastodon.social&quot;, &quot;@ExtinctionR@social.rebellion.global&quot;, &quot;@ptua@mastodon.social&quot;]">
<h2>Follow these 5 accounts</h2>
<p>Copy the handles below, or download a CSV to import via your Mastodon server's
<strong>Preferences &rarr; Import and export &rarr; Import &rarr; Following list</strong>.
Prefer one click? Use the <a href="../mastodon-follow/">Follow on Mastodon</a> tool.</p>
<label class="bulk-follow__label" for="bulk-follow-lifestyle-hobbies">Native accounts in Lifestyle, Travel &amp; Hobbies</label>
<textarea id="bulk-follow-lifestyle-hobbies" class="bulk-follow__text" rows="6" readonly spellcheck="false">@grebert@mastodon.top
@CopernicusECMWF@masto.ai
@ecosia@mastodon.social
@ExtinctionR@social.rebellion.global
@ptua@mastodon.social</textarea>
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

