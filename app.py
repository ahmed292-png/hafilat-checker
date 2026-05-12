from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/check-status")
async def check_status(card_id: str):

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page(
            user_agent="Mozilla/5.0"
        )

        try:
            await page.goto(
                "https://admobility.gov.ae/en/pb-bus-service/hafilat-cards",
                timeout=60000
            )

            await page.wait_for_timeout(3000)

            await page.fill("input", card_id)

            await page.click("button")

            await page.wait_for_timeout(5000)

            result = await page.locator("body").inner_text()

            await browser.close()

            return {
                "success": True,
                "result": result[:1000]
            }

        except Exception as e:

            await browser.close()

            return {
                "success": False,
                "message": str(e)
            }
