import json 

config = {}

with open('example2.conf') as fh:

    for line in fh:
        print(line.split())
        if line == "\n" or line[0] =="#":
            print("leeg of comment")
            continue
        args = line.split()
        action, *args = line.split()

        if action == 'config':
            header  = ' '.join(args)
            if header not in config:
                config[header] = {}

        if action == 'edit':
            section = ' '.join(args).strip('"')
            if section not in config[header]:
                config[header][section] = {}

        if action == 'set':
            name  = args.pop(0)
            value = ' '.join(args).strip('"')
            config[header][section][name] = value

print(json.dumps(config, indent=4))