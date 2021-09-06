from amino.lib.util import device

sid = None

class Headers:
    def __init__(self, data = None, type = None, deviceId: str = "2271017D5F917B37DAC9C325B10542BC9B63109292D882729D1813D5355404380E2F1A699A34629C10", sig: str = None):
        if deviceId:
            dev = device.DeviceGenerator(deviceId=deviceId)
        else:
            dev = device.DeviceGenerator()

        headers = {
            "NDCDEVICEID": "2271017D5F917B37DAC9C325B10542BC9B63109292D882729D1813D5355404380E2F1A699A34629C10",
            "NDC-MSG-SIG": dev.device_id_sig,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": dev.user_agent,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        if data: headers["Content-Length"] = str(len(data))
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        if type: headers["Content-Type"] = type
        #if sig: headers["NDC-MSG-SIG"] = sig
        self.headers = headers

class AdBsd:
    def __init__(self):
        uid = None
        self.data = {
            "reward": {
                "ad_unit_id": "255884441431980_807351306285288",
                "credentials_type": "publisher",
                "custom_json": {
                    "hashed_user_id": None
                },
                "demand_type": "sdk_bidding",
                "event_id": None,
                "network": "facebook",
                "placement_tag": "default",
                "reward_name": "Amino Coin",
                "reward_valid": "true",
                "reward_value": 2,
                "shared_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f",
                "version_id": "1569147951493",
                "waterfall_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"
            },
            "app": {
                "bundle_id": "com.narvii.amino.master",
                "current_orientation": "portrait",
                "release_version": "3.4.33567",
                "user_agent": "Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"
            },
            "date_created": 1620295485,
            "session_id": "49374c2c-1aa3-4094-b603-1cf2720dca67",
            "device_user": {
                "country": "US",
                "device": {
                    "architecture": "aarch64",
                    "carrier": {
                        "country_code": 602,
                        "name": "Vodafone",
                        "network_code": 0
                    },
                    "is_phone": "true",
                    "model": "GT-S5360",
                    "model_type": "Samsung",
                    "operating_system": "android",
                    "operating_system_version": "29",
                    "screen_size": {
                        "height": 2260,
                        "resolution": 2.55,
                        "width": 1080
                    }
                },
                "do_not_track": "false",
                "idfa": "7495ec00-0490-4d53-8b9a-b5cc31ba885b",
                "ip_address": "",
                "locale": "en",
                "timezone": {
                    "location": "Asia\/Seoul",
                    "offset": "GMT+09: 00"
                },
                "volume_enabled": "true"
            }
        }
        self.headers = {
            "cookies": "__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
            "authorization": "Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="
        }
        if uid: self.data["reward"]["custom_json"]["hashed_user_id"] = uid
