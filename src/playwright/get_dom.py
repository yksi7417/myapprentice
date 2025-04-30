import traceback
from playwright.sync_api import sync_playwright, Error
import time


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # remember last URL so we only log once per distinct page
        last_url = {"value": None}

        def log_dom():
            try:
                url = page.url
                if url == last_url["value"]:
                    return
                last_url["value"] = url

                timestamp = time.strftime("%X")
                print(f"\n=== Page update @ {timestamp} — {url} ===")
                html = page.content()
                print(html, "…")   # truncate for brevity
            except Error:
                # if the page/browser is already closed, just ignore
                pass

        # two handlers: full navigations & DOMContentLoaded (for SPAs)
        def on_nav(frame):
            if frame == page.main_frame:
                log_dom()

        def on_dom():
            log_dom()

        page.on("framenavigated", on_nav)
        page.on("domcontentloaded", on_dom)

        # You can also catch pushState in single‐page apps if needed:
        page.add_init_script("""
        const _push = history.pushState;
        history.pushState = (...args) => {
            _push.apply(history, args);
            window.dispatchEvent(new Event('pushstate'));
        };
        """)
        page.evaluate("""
        window.addEventListener('pushstate', () => {
            // communicate back to Python via console
            console.debug('[SPA NAV]');
        });
        """)
        page.on("console", lambda msg: log_dom() if msg.type == "debug" and msg.text == "[SPA NAV]" else None)

        new_url = "https://example.com/login"
        try:
            while new_url != "q":
                page.goto(new_url, wait_until="networkidle")
                new_url = input("new_url here, or `q` to quit: ")
        except Exception as e:
            print("Exception type:", type(e).__name__)
            print("Exception module:", e.__class__.__module__)
            print("Exception message:", e)
            traceback.print_exc()
            print("\nExiting…")
        finally:
            browser.close()
            exit(1)


if __name__ == "__main__":
    main()
