# 🌩️ STORM – Smart Telemetry & Operational Recording for Mindstorm

**STORM** is a lightweight telemetry and logging system for LEGO Mindstorms EV3 robots. It monitors file-based sensor data, decodes it, and stores it in a structured format using the **MCAP** stream. It supports multiple connection types (USB, simulation, etc.) and decoding formats (protobuf, raw...).

## 🚀 Features
- Flexible connection to EV3 robots via a connector factory
- Pluggable data decoding via translator factory
- Continuous data recording using MCAP
- File change detection if append mode is used

## 📈 Model Documentations

- 🧩 [Block Definition Diagram (BDD)](diagram/definition_block_diagram.md)  
  > 💡 **Limitations on block definition diagram:**  
  > SysML stereotypes and properties are simplified and represented using basic Mermaid `class` syntax as Mermaid does not support SysML-specific distinctions between `class` vs `DataType` vs `Block`    

- 🔄 [Main Sequence Diagram](diagram/sequence_diagram.md)  
  > 💡 **Limitations on sequence diagram:**  
  > - The *lifelines*, *parts*, *blocks*, and *signals* are not clearly distinguished as Mermaid does not support blocks or signal events explicitly  
  > - No hierarchical structures (e.g., `Block:ConnectorFactory`) as Mermaid does not allow typing