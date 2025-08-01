###qXUmqtYkSM7lN26MYSKPURJKGXEtmH6F
###ru2cG4RnOxxwAqw6a4cwabBo1fHUxNsE
from fastapi import FastAPI, Depends
from api import send_notification_router , get_notification_router
from deps.api_key import get_api_key

app = FastAPI()

app.include_router(
    send_notification_router.router,
    dependencies=[Depends(get_api_key)]
    )

app.include_router(
    get_notification_router.router,
    dependencies=[Depends(get_api_key)]
    )
