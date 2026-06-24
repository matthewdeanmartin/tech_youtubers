/*
 * Creator profile page enhancements:
 *
 *  1. Lite-embed: clicking a video card's thumbnail swaps in the real YouTube
 *     iframe (privacy-friendly — no YouTube cookies until the visitor opts in).
 *     This runs on any page that has .video-card__play buttons.
 *
 *  2. Live Mastodon enrichment: when the visitor is logged in (token managed by
 *     follow-core.js), fetch this creator's recent public posts via the
 *     visitor's instance and render them, with lite-embed cards for any YouTube
 *     links. Logged-out visitors keep the static page unchanged.
 */
(function () {
  "use strict";

  /* ── 1. Lite-embed play buttons ─────────────────────────────────── */
  function wirePlayButtons(root) {
    (root || document).querySelectorAll(".video-card__play").forEach(function (btn) {
      if (btn.dataset.wired) return;
      btn.dataset.wired = "1";
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-video-id");
        var title = btn.getAttribute("data-video-title") || "YouTube video";
        if (!id) return;
        var iframe = document.createElement("iframe");
        iframe.className = "video-card__iframe";
        iframe.width = "320";
        iframe.height = "180";
        iframe.loading = "lazy";
        iframe.allow =
          "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.allowFullscreen = true;
        iframe.title = title;
        // youtube-nocookie keeps the privacy promise even after opt-in.
        iframe.src =
          "https://www.youtube-nocookie.com/embed/" +
          encodeURIComponent(id) +
          "?autoplay=1";
        btn.replaceWith(iframe);
      });
    });
  }

  /* ── 2. Live Mastodon enrichment ────────────────────────────────── */
  var MF = window.MastodonFollow;

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  // Pull YouTube video ids out of a status's HTML content + cards.
  function videoIdsFromStatus(status) {
    var ids = [];
    var re = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([0-9A-Za-z_-]{11})/g;
    var hay = (status.content || "") + " " + (status.card ? status.card.url || "" : "");
    var m;
    while ((m = re.exec(hay)) !== null) {
      if (ids.indexOf(m[1]) === -1) ids.push(m[1]);
    }
    return ids;
  }

  function liteCard(id) {
    return (
      '<li class="video-card">' +
      '<button type="button" class="video-card__play" data-video-id="' +
      escapeHtml(id) +
      '" data-video-title="YouTube video" aria-label="Play video">' +
      '<img class="video-card__thumb" src="https://i.ytimg.com/vi/' +
      escapeHtml(id) +
      '/mqdefault.jpg" alt="" loading="lazy" width="320" height="180" />' +
      '<span class="video-card__badge" aria-hidden="true">▶</span>' +
      "</button></li>"
    );
  }

  function renderStatus(status) {
    var when = status.created_at ? status.created_at.slice(0, 10) : "";
    var ids = videoIdsFromStatus(status);
    var cards = ids.length
      ? '<ul class="video-cards__grid">' + ids.map(liteCard).join("") + "</ul>"
      : "";
    // status.content is sanitized HTML from the Mastodon API; render as-is.
    return (
      '<li class="creator-post">' +
      '<div class="creator-post__body">' +
      (status.content || "") +
      "</div>" +
      cards +
      (status.url
        ? '<a class="creator-post__permalink" href="' +
          escapeHtml(status.url) +
          '" target="_blank" rel="noopener noreferrer">' +
          (when || "View post") +
          "</a>"
        : "") +
      "</li>"
    );
  }

  async function enrichCreator(section) {
    if (!MF || !MF.isConnected()) return; // logged-out: leave static page as-is.
    var acct = section.getAttribute("data-mastodon-acct");
    if (!acct) return;
    var hint = section.querySelector("[data-creator-live-hint]");
    var feed = section.querySelector("[data-creator-live-feed]");
    if (hint) hint.textContent = "Loading recent posts…";

    try {
      var account = await MF.resolveAccount(acct);
      var statuses = await MF.accountStatuses(account.id, { limit: 10 });
      if (hint) hint.hidden = true;
      if (!statuses.length) {
        if (hint) {
          hint.hidden = false;
          hint.textContent = "No recent public posts.";
        }
        return;
      }
      feed.innerHTML =
        '<ul class="creator-posts">' + statuses.map(renderStatus).join("") + "</ul>";
      feed.hidden = false;
      wirePlayButtons(feed);
    } catch (e) {
      if (hint) {
        hint.hidden = false;
        hint.textContent = "Could not load posts: " + (e && e.message ? e.message : e);
      }
    }
  }

  function start() {
    wirePlayButtons(document);
    var section = document.querySelector("[data-creator-live]");
    if (section) {
      // verifyCredentials (run by header-auth) may still be in flight; a tick
      // later isConnected() is reliable. Re-check on a microtask.
      Promise.resolve().then(function () { enrichCreator(section); });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
