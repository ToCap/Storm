sequenceDiagram
    participant Main
    participant ConnectorFactory
    participant TranslatorFactory
    participant MCAPStream
    participant Connector
    participant Translator

    Main->>ConnectorFactory: create("sim", ...)
    ConnectorFactory-->>Main: Connector instance

    Main->>TranslatorFactory: create("proto")
    TranslatorFactory-->>Main: Translator instance

    Main->>MCAPStream: instantiate
    MCAPStream-->>Main: mcap instance

    loop while True
        Main->>Connector: list_files("prjs/*.txt")
        Connector-->>Main: [(name, size), ...]

        loop for each file
            Main->>Main: process_file(name, size, ...)

            alt file not in files_dict
                Main->>Main: init files_dict[name]
            end

            Main->>Connector: is_append_mode()
            Connector-->>Main: mode

            alt size > 0 and changed
                Main->>Connector: read_file("prjs/{name}")
                Connector-->>Main: content

                alt content and new hash
                    Main->>Translator: decode(topic, content)
                    Translator-->>Main: decoded

                    Main->>MCAPStream: write("log", topic, decoded, ...)
                else content is None
                    Main->>Main: print("⚠️ Read error")
                end
            else
                Main->>Main: print("🔁 File unchanged")
            end
        end
    end

    alt Exception occurs
        Main->>Main: print("❌ Error retrieving files")
    else KeyboardInterrupt
        Main->>Main: exit gracefully
    end

