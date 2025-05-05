import asyncio
from bleak import BleakClient

# Direccion MAC de ESP32
ESP32_ADDRESS = "XX:XX:XX:XX:XX:XX"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def eraser():
    async with BleakClient(ESP32_ADDRESS) as client:
        print("Conectado al ESP32")

        # Enviar comando al ESP32
        msg = "ERASER"
        await client.write_gatt_char(CHARACTERISTIC_UUID, msg.encode())
        print("Comando enviado: ", msg)

        # Leer respuesta
        response = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print("Respuesta del ESP32:", response.decode())

        return response.decode()

