from pydantic import BaseModel


class Image64(BaseModel):
    screenshot: str


class Coordinate(BaseModel):
    x: int
    y: int
    

class Position(BaseModel):
    top_left: Coordinate
    bottom_right: Coordinate


class Button(BaseModel):
    name: str
    content: str
    coordinate: Position


class Notification(BaseModel):
    order: int
    type: str
    coordinate: Position
    buttons: list[Button]


class NotificationList(BaseModel):
    notification_windows: list[Notification]


request_examples = {
    "overlapping": {
        "summary": "Overlapping site notifications",
        "description": "Screenshot contains two site notifications and back notification is closable",
        "value": {
            "screenshot": open("binary_example1.txt").read()
        },
    },
    "system": {
        "summary": "System notification",
        "description": "Single system notification with 2 buttons: confirm and not confirm",
        "value": {
            "screenshot": open("binary_example2.txt").read()
        },
    },
    "invalid": {
        "summary": "Invalid data",
        "description": "An input string must be convertable to image otherwise a String Convertion Error will be raised",
        "value": {
            "screenshot": "Foo bar"
        },
    }
}


response_examples = {
    200: {
        "content": {
            "application/json": {
                "examples": {
                    "overlapping": {
                            "summary": "Overlapping site notifications",
                            "description": "There are two site notifications and back notification is closable",
                            "value": {
                                "notification_windows": [
                                    {
                                        "order": 1,
                                        "type": "site",
                                        "coordinate": {
                                            "top_left": {
                                                "x": 259,
                                                "y": 1375
                                            },
                                            "bottom_right": {
                                                "x": 946,
                                                "y": 1802
                                            }
                                        },
                                        "buttons": [
                                            {
                                                "name": "close",
                                                "content": "",
                                                "coordinate": {
                                                    "top_left": {
                                                        "x": 860,
                                                        "y": 1392
                                                    },
                                                    "bottom_right": {
                                                        "x": 930,
                                                        "y": 1461
                                                    }
                                                }
                                            }
                                        ]
                                    },
                                {
                                    "order": 2,
                                    "type": "site",
                                    "coordinate": {
                                        "top_left": {
                                            "x": 107,
                                            "y": 860
                                        },
                                        "bottom_right": {
                                            "x": 962,
                                            "y": 1594
                                        }
                                    },
                                    "buttons": [
                                        {
                                            "name": "close",
                                            "content": "",
                                            "coordinate": {
                                                "top_left": {
                                                    "x": 849,
                                                    "y": 886
                                                },
                                                "bottom_right": {
                                                    "x": 940,
                                                    "y": 983
                                                }
                                            }
                                        },
                                        {
                                            "name": "confirm",
                                            "content": "",
                                            "coordinate": {
                                                "top_left": {
                                                    "x": 342,
                                                    "y": 1214
                                                },
                                                "bottom_right": {
                                                    "x": 738,
                                                    "y": 1349
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                    },
                    "system": {
                        "summary": "System notification",
                        "description": "Single system notification with 2 buttons: confirm and not confirm",
                        "value": {
                            "notification_windows": [
                                {
                                    "order": 1,
                                    "type": "system",
                                    "coordinate": {
                                        "top_left": {
                                            "x": 5,
                                            "y": 281
                                        },
                                        "bottom_right": {
                                            "x": 301,
                                            "y": 430
                                        }
                                    },
                                    "buttons": [
                                        {
                                            "name": "NOT_confirm",
                                            "content": "",
                                            "coordinate": {
                                                "top_left": {
                                                    "x": 113,
                                                    "y": 379
                                                },
                                                "bottom_right": {
                                                    "x": 204,
                                                    "y": 413
                                                }
                                            }
                                        },
                                        {
                                            "name": "confirm",
                                            "content": "",
                                            "coordinate": {
                                                "top_left": {
                                                    "x": 210,
                                                    "y": 379
                                                },
                                                "bottom_right": {
                                                    "x": 287,
                                                    "y": 411
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                }
            }
        }
    },
    400: {
        "description": "String Convertion Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not convert input string to image"
                }
            }
        }
    }
}