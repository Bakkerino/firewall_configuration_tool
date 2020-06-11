import json 

debug = True
with open('develop_backlog_and_testing\parser\example2.conf') as fh:
        
        arguments = ['system', 'vpn', 'user', 'vdom', 'firewall', 'voip', 'web-proxy', 'application', 'dlp', 'webfilter']
        config = {}
        previous_line = []
        section = ""
        count = 0
        for line in fh:
            if debug:
                count += 1
                current_line = line.split()
                print("###########################################")
                print(count - 1, ": Previous line: >", previous_line)
                print(count, ": Current line: >", current_line)

            if line[0] in ("#", "\n"):
                if debug: print("empty/comment")
                continue

            args = line.split()
            action, *args = line.split()

            if action == 'config' and args[0] in arguments:

                if args[0] == 'system': args.pop(0)
                header = ' '.join(args)
                if header not in config:
                    config[header] = {}
            else:
                pass

            if action == 'edit':
                section = ' '.join(args).strip('"')
                if section not in config[header]:
                    config[header][section] = {}

            if action == 'set':
                if previous_line[0] == 'config' and section not in config[header]:
                    section = '1'
                    config[header][section] = {}

                name  = args.pop(0)
                value = ' '.join(args).strip('"')
                if value.startswith('-----'):
                    value += " "
                    for line in fh:
                        if line.startswith('-----'): value += " " + ' '.join(line.split()).strip('"'); break
                        else: value += ' '.join(line.split()).strip('"')
                config[header][section][name] = value


            if action == 'append':
                name  = args.pop(0)
                value = ' '.join(args).strip('"')
                config[header][section][name] = value

            previous_line = line.split()



print(json.dumps(config, indent=4))