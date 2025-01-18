from api.controllers import market_controller as market
from api.controllers import alert_controller as alert
from api.controllers import rule_controller as rule

def init_routes(app):
    app.include_router(market.router)
    app.include_router(rule.router)
    app.include_router(alert.router)
    return app
