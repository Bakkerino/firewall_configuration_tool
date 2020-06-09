import json 


with open('example2.conf') as fh:
    config = {}
    previous_line = []
    for line in fh:
        current_line = line.split()
        print("-------------------")
        print("Previous line: >")
        print(previous_line)
        print("Current line: >")
        print(current_line)
        if line == "\n" or line[0] == "#":
            print("leeg of comment")
            continue
        args = line.split()
        action, *args = line.split()

        if action == 'config' and args[0] == 'system':
            header  = ' '.join(args)
            if header not in config:
                config[header] = {}

        if action == 'edit':
            section = ' '.join(args).strip('"')
            if section not in config[header]:
                config[header][section] = {}
        # Waardes
        if action == 'set':
            name  = args.pop(0)
            value = ' '.join(args).strip('"')
            config[header][section][name] = value

        if action == 'append':
            name  = args.pop(0)
            value = ' '.join(args).strip('"')
            config[header][section][name] = value

        previous_line = line.split()


print(json.dumps(config, indent=4))