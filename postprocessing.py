from ultralytics.engine.results import Boxes, Results


cls_alias = {0: "", 1: "close", 2: "confirm", 3: "NOT_confirm", 4: "site", 5: "system"}


def get_alert_info(alert: Boxes) -> dict:
    alert_info = {
        "order": 1,
        "type": cls_alias[alert.cls[0]],
        "coordinate": {
            "top_left": {
                "x": round(alert.xyxy[0][0]),
                "y": round(alert.xyxy[0][1])
            },
            "bottom_right": {
                "x": round(alert.xyxy[0][2]),
                "y": round(alert.xyxy[0][3])
            }
        },
        "buttons": []
    }
    return alert_info


def get_button_info(button: Boxes) -> dict:
    button_info = {
        "name": cls_alias[button.cls[0]],
        "content": "",
        "coordinate": {
            "top_left": {
                "x": round(button.xyxy[0][0]),
                "y": round(button.xyxy[0][1])
            },
            "bottom_right": {
                "x": round(button.xyxy[0][2]),
                "y": round(button.xyxy[0][3])
            }
        }
    }
    return button_info


def are_overlapping_boxes(box1: Boxes, box2: Boxes) -> bool:
    x1_1, y1_1, x2_1, y2_1 = box1.xyxy[0]
    x1_2, y1_2, x2_2, y2_2 = box2.xyxy[0]

    if y2_2 <= y1_1 or y1_2 >= y2_1 or x1_2 >= x2_1 or x2_2 <= x1_1:
        return False
    return True


def are_overlapping_alerts(alert1: dict, alert2: dict) -> bool:
    x1_1, y1_1 = alert1["coordinate"]["top_left"]["x"], alert1["coordinate"]["top_left"]["y"]
    x2_1, y2_1 = alert1["coordinate"]["bottom_right"]["x"], alert1["coordinate"]["bottom_right"]["y"]
    x1_2, y1_2 = alert2["coordinate"]["top_left"]["x"], alert2["coordinate"]["top_left"]["y"]
    x2_2, y2_2 = alert2["coordinate"]["bottom_right"]["x"], alert2["coordinate"]["bottom_right"]["y"]

    if y2_2 <= y1_1 or y1_2 >= y2_1 or x1_2 >= x2_1 or x2_2 <= x1_1:
        return False
    return True


def get_square(alert: dict) -> float:
    w = alert["coordinate"]["bottom_right"]["x"] - alert["coordinate"]["top_left"]["x"]
    h = alert["coordinate"]["bottom_right"]["y"] - alert["coordinate"]["top_left"]["y"]
    return w * h


def closable_back_alert(alert: dict) -> bool:
    if alert["order"] == 1:
        return True
    for button in alert["buttons"]:
        if button["name"] in ("close", "confirm", "NOT_confirm"):
            return True
    return False


def process_results(inputs: list[Results]) -> dict:
    boxes = inputs[0].boxes.cpu().numpy()

    alerts = []
    buttons = []
    for box in boxes:
        if box.cls[0] in (4, 5):  # 4: 'site_alert', 5: 'system_alert'
            alerts.append(box)
        elif box.cls[0] in (0, 1, 2, 3):  # 0: 'button', 1: 'close_button', 2: 'confirm_button', 3: 'not_confirm_button'
            buttons.append(box)
    
    notification_windows = []
    for alert in alerts:
        alert_info = get_alert_info(alert)
        for button in buttons:
            if are_overlapping_boxes(alert, button):
                alert_info["buttons"].append(get_button_info(button))
        notification_windows.append(alert_info)
    
    # Check overlapping alerts
    # Assumption: Foreground notifications are assumed to have a smaller area. Otherwise they are difficult to detect.
    for idx, alert in enumerate(notification_windows):
        for other in notification_windows[idx + 1:]:
            if are_overlapping_alerts(alert, other):
                if get_square(alert) >= get_square(other):
                    alert["order"] += 1
                    alert["buttons"] = list(filter(lambda x: x not in other["buttons"], alert["buttons"]))
                else:
                    other["order"] += 1
                    other["buttons"] = list(filter(lambda x: x not in alert["buttons"], other["buttons"]))

    # Check if back alert has close/confirm/not_confirm button
    notification_windows = list(filter(closable_back_alert, notification_windows))

    return {"notification_windows": notification_windows}
