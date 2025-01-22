from app.api.controllers import market_controller as market
from app.api.controllers import alert_controller as alert
from app.api.controllers import alert_rule_controller as alert_rule

def init_routes(app):
    app.include_router(market.router)
    app.include_router(alert_rule.router)
    app.include_router(alert.router)
    return app
