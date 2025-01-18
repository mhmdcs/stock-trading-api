from api.controllers import market_controller as market
# from api.controllers import alert_controller as rule
# from api.controllers import alert_rule_controller as alert_rule

def init_routes(app):
    app.include_router(market.router)
    # app.include_router(rule.router)
    # app.include_router(alert_rule.router)
    return app
