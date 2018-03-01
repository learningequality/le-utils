# Detect RTL languages bases on the first native_name our languagelookup.json
# Outpus a list of internal language codes: 
# INSTALL:
#   sudo gem install string-direction
#   sudo gem install json
#
# USAGE
#   ruby direction_guessed.rb

require 'json'
require 'string-direction'
detector = StringDirection::Detector.new
# ^^^^^^ uses various heuristics to guess language direction
# see https://github.com/waiting-for-dev/string-direction

file = File.read('../le_utils/resources/languagelookup.json')
langs = JSON.parse(file)

puts 'RTL_LANG_CODES = ['
langs.each do |code, info|
  name = info["name"] 
  native_name = info["native_name"]
  # choose only the first part in cases where native_name is list-like
  first_native_name = native_name.split(',')[0].split('()')[0]
  dir = detector.direction(first_native_name)
  if dir.nil?
    dir='Unknown'
    puts code + ' '  + name
  end
  if dir == 'rtl'
    puts '    "' + code +  '",  # ' + name
    # puts '{"le_code":"' + code +  '", "dir":"' + dir + '", "first_native_name":"' + first_native_name + '", "native_name":"' + native_name +  '", "name":' + name + '"},'
  end
end
puts ']'
    