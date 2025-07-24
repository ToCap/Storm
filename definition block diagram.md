classDiagram

    %% === Enumerations ===
    class InfraredSensorModes {
        <<enumeration>>
        + PROXIMITY
        + DETECTED
        + HEADING
    }

    class TouchSensorModes {
        <<enumeration>>
        + MEASURE
        + COMPARE
    }

    class TouchSensorStates {
        <<enumeration>>
        + RELEASED
        + PRESSED
        + BUMPED
    }

    class OdometrySensorModes {
        <<enumeration>>
        + MEASURE
        + COMPARE
    }

    %% === Infrared Sensor Payloads ===
    class ProximityData {
        + value : Integer
    }

    class DetectedData {
        + state : Boolean
    }

    class HeadingData {
        + heading : Integer
    }

    class InfraredPayload {
        <<union>>
        + proximity : ProximityData
        + detected  : DetectedData
        + heading   : HeadingData
    }

    class InfraredSensorData {
        + timestamp : Integer
        + mode : InfraredSensorModes
        + payload : InfraredPayload
    }

    %% === Touch Sensor Payloads ===
    class MeasureData {
        + state : Boolean
    }

    class CompareData {
        + result : Boolean
        + measure : TouchSensorStates
    }

    class TouchPayload {
        <<union>>
        + measure : MeasureData
        + compare : CompareData
    }

    class TouchSensorData {
        + timestamp : Integer
        + mode : TouchSensorModes
        + payload : TouchPayload
    }

    %% === Odometry Sensor Data ===
    class OdometrySensorData {
        + timestamp : Integer
        + mode : OdometrySensorModes
        + degrees : Integer
        + rotations : Integer
        + cuurentPower : Integer
    }

    %% === Associations ===

    %% Infrared
    InfraredSensorData --> InfraredSensorModes
    InfraredSensorData --> InfraredPayload
    InfraredPayload --> ProximityData
    InfraredPayload --> DetectedData
    InfraredPayload --> HeadingData

    %% Touch
    TouchSensorData --> TouchSensorModes
    TouchSensorData --> TouchPayload
    TouchPayload --> MeasureData
    TouchPayload --> CompareData
    CompareData --> TouchSensorStates

    %% Odometry
    OdometrySensorData --> OdometrySensorModes
