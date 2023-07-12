# Author: Sakthi Santhosh
# Created on: 11/05/2023
def main() -> int:
    from time import sleep

    from lib import inferrer_handle, telemetry_handle

    while True:
        try:
            image_array = inferrer_handle.capture()
            result = inferrer_handle.infer(image_array)

            telemetry_handle.post(result)
            sleep(10)
        except KeyboardInterrupt:
            print("\rExit")
            return 0
        except:
            return 1

if __name__ == "__main__":
    exit(main())
