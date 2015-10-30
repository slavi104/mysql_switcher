from config import *

def dump_db(params=['LOCAL', 'switch', 'update']):
	print()
	# set params in variables
	if params[1] in list(DATABASES.keys()):
		db_label = params[1]
	else:
		print('Please select DB!')
		print(list(DATABASES.keys()))
		return False
	
	# Switch
	force_switch = False
	if 'switch' in params:
		force_switch = True

	# Update
	force_update = False
	if 'update' in params:
		force_update = True

	remote_db = DATABASES[db_label]
	date_time = time.strftime('%Y-%m-%d_%X')
	local_db = DATABASES['LOCAL']
	backup_db_name = local_db['NAME'] + '_' + db_label
	main_db_name = local_db['NAME']
	remote_pass = ''
	local_pass = ''

	if len(remote_db['PASSWORD']):
		remote_pass = ' -p {}'.format(remote_db['PASSWORD'])
	if len(local_db['PASSWORD']):
		local_pass = ' -p {}'.format(local_db['PASSWORD'])

	print('Connecting to local DB server ...')
	conn = pymysql.connect(
		host=local_db['HOST'], 
		port=local_db['PORT'], 
		user=local_db['USERNAME'], 
		passwd=local_db['PASSWORD']
	)
	cur = conn.cursor()
	print('Connected to local DB server!')

	# if we don't have backup lets make one
	if 0 == cur.execute("SHOW DATABASES LIKE '{}';".format(backup_db_name)):
		print('Local backup {} does not exist!'.format(backup_db_name))
		print('Creating local backup of {} DB...'.format(db_label))
		force_update = True

	# UPDATE LOCAL BACKUP
	if force_update:
		print()
		print('Updating...')
		# shell commands string
		shell_command_backup = 'mysqldump -h {} -P {} -u {}{} {} | mysql -h {} -P {} -u {}{} {}'.format(
			remote_db['HOST'],
			remote_db['PORT'],
			remote_db['USERNAME'],
			remote_pass,
			remote_db['NAME'],
			local_db['HOST'],
			local_db['PORT'],
			local_db['USERNAME'],
			local_pass,
			backup_db_name
		)

		print('Connecting to remote ({}) server ...'.format(db_label))
		try:
			cur.execute('CREATE DATABASE {};'.format(backup_db_name))
			print('Creating new local backup {} ...'.format(backup_db_name))
		except Exception:
			cur.execute('DROP DATABASE {};'.format(backup_db_name))
			cur.execute('CREATE DATABASE {};'.format(backup_db_name))
			print('Updating local backup {} ...'.format(backup_db_name))
		
		print('Coping remote {} DB to local {} backup ...'.format(db_label, backup_db_name))
		backup = subprocess.Popen(shell_command_backup, shell=True)
		backup.wait()
		print('Updating of local backup finished!')

	# SWITCH MAIN DB TO ANY OF LOCALS
	if force_switch:
		print()
		print('Switching...')
		try:
			cur.execute('DROP DATABASE {};'.format(main_db_name))
			print('Deleting local main DB {} ...'.format(main_db_name))
		except Exception:
			print('{} DB does not exist locally!'.format(main_db_name))
		
		print('Creating local main DB {} ...'.format(main_db_name))
		cur.execute('CREATE DATABASE {};'.format(main_db_name))

		print('Coping from {} to local {} ...'.format(backup_db_name, main_db_name))
		shell_command_main = 'mysqldump -h {} -P {} -u {}{} {} | mysql -h {} -P {} -u {}{} {}'.format(
			local_db['HOST'],
			local_db['PORT'],
			local_db['USERNAME'],
			local_pass,
			backup_db_name,
			local_db['HOST'],
			local_db['PORT'],
			local_db['USERNAME'],
			local_pass,
			main_db_name
		)
			
		# subprocess for 
		main = subprocess.Popen(shell_command_main, shell=True)
		main.wait()
		print('Switching to {} DB finished!'.format(db_label))

	print()
	print('DONE!')
	return True


if __name__ == "__main__":

	if len(sys.argv) > 1:
		dump_db(sys.argv)
	else:
		print('Please, add first parameter server label!')
