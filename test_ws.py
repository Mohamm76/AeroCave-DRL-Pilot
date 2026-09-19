import asyncio
import websockets
import json

async def test_telemetry():
    uri = "ws://127.0.0.1:8000/ws/telemetry"
    print("🔌 جاري الاتصال بخادم الـ WebSocket...")
    
    async with websockets.connect(uri) as websocket:
        print("✅ تم الاتصال بنجاح! جاري استقبال أول 5 حزم من بيانات البث الحي:\n")
        for i in range(5):
            message = await websocket.recv()
            data = json.loads(message)
            print(f"📦 حزمة [{i+1}]: Step={data['step']} | Pos=({data['position']['x']:.2f}, {data['position']['y']:.2f}, {data['position']['z']:.2f}) | Battery={data['telemetry']['battery']}% | Status={data['telemetry']['status']}")

if __name__ == "__main__":
    asyncio.run(test_telemetry())