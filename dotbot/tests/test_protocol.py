import pytest


from dotbot.protocol import (
    PayloadType,
    ProtocolPayload,
    ProtocolPayloadParserException,
    ProtocolHeader,
    CommandMoveRaw,
    CommandRgbLed,
    Advertisement,
    Lh2RawLocation,
    Lh2RawData,
    LH2Location,
    GPSPosition,
    DotBotData,
)


@pytest.mark.parametrize(
    "payload,expected",
    [
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x34\x00\x01\x00\x00\x42\x00\x42",
            ProtocolPayload(
                ProtocolHeader(0x1122221111111111, 0x1212121212121212, 0x1234, 0, 1),
                PayloadType.CMD_MOVE_RAW,
                CommandMoveRaw(0, 66, 0, 66),
            ),
            id="MoveRaw",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x34\x00\x01\x01\x42\x42\x42",
            ProtocolPayload(
                ProtocolHeader(0x1122221111111111, 0x1212121212121212, 0x1234, 0, 1),
                PayloadType.CMD_RGB_LED,
                CommandRgbLed(66, 66, 66),
            ),
            id="RGBLed",
        ),
        pytest.param(
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02",
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.LH2_RAW_DATA,
                Lh2RawData(
                    [
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                    ],
                ),
            ),
            id="LH2RawData",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x34\x00\x01\x03"
            b"\x00\x00\x03\xe8\x00\x00\x03\xe8\x00\x00\x00\x02",
            ProtocolPayload(
                ProtocolHeader(0x1122221111111111, 0x1212121212121212, 0x1234, 0, 1),
                PayloadType.LH2_LOCATION,
                LH2Location(1000, 1000, 2),
            ),
            id="LH2Location",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x34\x00\x01\x04",
            ProtocolPayload(
                ProtocolHeader(0x1122221111111111, 0x1212121212121212, 0x1234, 0, 1),
                PayloadType.ADVERTISEMENT,
                Advertisement(),
            ),
            id="Advertisement",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x34\x00\x01\x05"
            b"&~\xe9\x02]\xe4#\x00",
            ProtocolPayload(
                ProtocolHeader(0x1122221111111111, 0x1212121212121212, 0x1234, 0, 1),
                PayloadType.GPS_POSITION,
                GPSPosition(48856614, 2352221),  # Paris coordinates
            ),
            id="GPSPosition",
        ),
        pytest.param(
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x06"
            b"-\x00"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02",
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.DOTBOT_DATA,
                DotBotData(
                    direction=45,
                    locations=[
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                        Lh2RawLocation(0xF1DEBC9A78563412, 0x01, 0x02),
                    ],
                ),
            ),
            id="DotBotData",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x00\x00\x00\x01\xff",
            ValueError(),
            id="invalid payload",
        ),
        pytest.param(
            b"\x11\x22\x22\x11\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x00\x00\x00\x01\x07",
            ProtocolPayloadParserException(),
            id="unsupported payload type",
        ),
    ],
)
def test_protocol_parser(payload, expected):
    if isinstance(expected, Exception):
        with pytest.raises(expected.__class__):
            _ = ProtocolPayload.from_bytes(payload)
    else:
        protocol = ProtocolPayload.from_bytes(payload)
        assert protocol.header == expected.header
        assert protocol.payload_type == expected.payload_type
        assert protocol.values == expected.values


@pytest.mark.parametrize(
    "payload,expected",
    [
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_MOVE_RAW,
                CommandMoveRaw(0, 66, 0, 66),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x00\x00\x42\x00\x42",
            id="MoveRaw1",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_MOVE_RAW,
                CommandMoveRaw(0, 0, 0, 0),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x00\x00\x00\x00\x00",
            id="MoveRaw2",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_MOVE_RAW,
                CommandMoveRaw(-10, -10, -10, -10),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x00\xf6\xf6\xf6\xf6",
            id="MoveRaw3",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_RGB_LED,
                CommandRgbLed(0, 0, 0),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x01\x00\x00\x00",
            id="RGBLed1",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_RGB_LED,
                CommandRgbLed(255, 255, 255),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x01\xff\xff\xff",
            id="RGBLed2",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.LH2_RAW_DATA,
                Lh2RawData(
                    [
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                    ],
                ),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02",
            id="LH2RawData",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.LH2_LOCATION,
                LH2Location(1000, 1000, 2),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x03"
            b"\xe8\x03\x00\x00\xe8\x03\x00\x00\x02\x00\x00\x00",
            id="LH2Location",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.ADVERTISEMENT,
                Advertisement(),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x04",
            id="Advertisement",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.GPS_POSITION,
                GPSPosition(48856614, 2352221),  # Paris coordinates
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x05"
            b"\x02\xe9~&\x00#\xe4]",
            id="GPSPosition",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.DOTBOT_DATA,
                DotBotData(
                    direction=45,
                    locations=[
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                    ],
                ),
            ),
            b"\x11\x22\x33\x44\x55\x66\x77\x88\x12\x22\x12\x22\x12\x22\x12\x21\x24\x42\x00\x01\x06"
            b"\x00-"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02"
            b"\x12\x34\x56\x78\x9a\xbc\xde\xf1\x01\x02",
            id="DotBotData",
        ),
    ],
)
def test_payload(payload, expected):
    result = payload.to_bytes()
    assert result == expected, f"{result} != {expected}"


@pytest.mark.parametrize(
    "payload,string",
    [
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_MOVE_RAW,
                CommandMoveRaw(0, 66, 0, 66),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------+------+------+------+\n"
                " CMD_MOVE_RAW    | dst                              | src                              | swarm id | app. | ver. | type | lx   | ly   | rx   | ry   |\n"
                " (25 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x00 | 0x00 | 0x42 | 0x00 | 0x42 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------+------+------+------+\n"
                "\n"
            ),
            id="MoveRaw",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.CMD_RGB_LED,
                CommandRgbLed(0, 0, 0),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------+------+------+\n"
                " CMD_RGB_LED     | dst                              | src                              | swarm id | app. | ver. | type | red  | green| blue |\n"
                " (24 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x01 | 0x00 | 0x00 | 0x00 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------+------+------+\n"
                "\n"
            ),
            id="RGBLed",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.LH2_RAW_DATA,
                Lh2RawData(
                    [
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                    ],
                ),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                " LH2_RAW_DATA    | dst                              | src                              | swarm id | app. | ver. | type |\n"
                " (41 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x02 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                "                 +----------------------------------+------+------+----------------------------------+------+------+\n"
                "                 | bits                             | poly | off. | bits                             | poly | off. |\n"
                "                 | 0x123456789abcdef1               | 0x01 | 0x02 | 0x123456789abcdef1               | 0x01 | 0x02 |\n"
                "                 +----------------------------------+------+------+----------------------------------+------+------+\n"
                "\n"
            ),
            id="LH2RawData",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.LH2_LOCATION,
                LH2Location(1000, 1000, 2),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                " LH2_LOCATION    | dst                              | src                              | swarm id | app. | ver. | type |\n"
                " (33 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x03 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                "                 +------------------+------------------+------------------+\n"
                "                 | x                | y                | z                |\n"
                "                 | 0xe8030000       | 0xe8030000       | 0x02000000       |\n"
                "                 +------------------+------------------+------------------+\n"
                "\n"
            ),
            id="LH2Location",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.ADVERTISEMENT,
                Advertisement(),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                " ADVERTISEMENT   | dst                              | src                              | swarm id | app. | ver. | type |\n"
                " (21 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x04 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                "\n"
            ),
            id="Advertisement",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.GPS_POSITION,
                GPSPosition(48856614, 2352221),  # Paris coordinates
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------------------+------------------+\n"
                " GPS_POSITION    | dst                              | src                              | swarm id | app. | ver. | type | latitude         | longitude        |\n"
                " (29 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x05 | 0x02e97e26       | 0x0023e45d       |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+------------------+------------------+\n"
                "\n"
            ),
            id="GPSPosition",
        ),
        pytest.param(
            ProtocolPayload(
                ProtocolHeader(0x1122334455667788, 0x1222122212221221, 0x2442, 0, 1),
                PayloadType.DOTBOT_DATA,
                DotBotData(
                    direction=45,
                    locations=[
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                        Lh2RawLocation(0x123456789ABCDEF1, 0x01, 0x02),
                    ],
                ),
            ),
            (
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                " DOTBOT_DATA     | dst                              | src                              | swarm id | app. | ver. | type |\n"
                " (43 Bytes)      | 0x1122334455667788               | 0x1222122212221221               | 0x2442   | 0x00 | 0x01 | 0x06 |\n"
                "                 +----------------------------------+----------------------------------+----------+------+------+------+\n"
                "                 +----------+----------------------------------+------+------+----------------------------------+------+------+\n"
                "                 | dir.     | bits                             | poly | off. | bits                             | poly | off. |\n"
                "                 | 0x002d   | 0x123456789abcdef1               | 0x01 | 0x02 | 0x123456789abcdef1               | 0x01 | 0x02 |\n"
                "                 +----------+----------------------------------+------+------+----------------------------------+------+------+\n"
                "\n"
            ),
            id="DotBotData",
        ),
    ],
)
def test_payload_repr(payload, string, capsys):
    print(payload)
    out, _ = capsys.readouterr()
    assert out == string
