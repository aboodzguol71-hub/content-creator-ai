def plan_social_post(topic: str, platform: str, script: str):
    return {
        "platform": platform,
        "topic": topic,
        "hook": f"هل تعرف أن {topic} أصبح أحد أهم المواضيع اليوم؟",
        "body": script[:180],
        "hashtags": [
            "#عربي",
            "#محتوى",
            "#تسويق",
            "#تكنولوجيا",
            f"#{platform.replace(' ', '').replace('/', '')}",
        ],
        "recommended_length": "15-30 ثانية",
        "status": "ready_for_review",
    }
