def review(request):
    missing = []
    if request.get("environment") == "prod":
        missing.append("policy")
    if request.get("monthly_cost", 0) > request.get("cost_cap", 0):
        missing.append("cost_ok")
    if not request.get("citation"):
        missing.append("citation")
    image = request.get("image", "")
    if ":" not in image or image.endswith(":latest"):
        missing.append("pinned_image")
    if missing:
        return {"status": "blocked", "missing": missing, "live": False}
    return {"status": "ready_for_readout", "missing": [], "live": False}
