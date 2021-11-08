--[[--------------------------------------------------
Copyright (c) 2020,2021 TSP DATA, a.s. All rights reserved.

Amon Robot script for configurabe HTTP(s) testing
v1.3

--]]--------------------------------------------------

-- modules ----------------------------------
local amon = require("amon")
local http = require("http")
local yaml = require("yaml")
local jsonpath = require("jsonpath")
local xmlpath = require("xmlpath")
local re = require("re")


-- constants ----------------------------------
cfg_fname = "tests.yaml"  -- configuration file name
list_fname = "tests.list"  -- list file name (file containing list of configuration parts)
err_cfg_exit_code = 1      -- error code in case of configuraton error
err_cfg_reason = 100      -- reason in case of configuraton error
reason_metric = "reason"  -- name of the reason metric

-- default configuration values
defaults_cfg = "defaults"
variables_cfg = "variables"
steps_cfg = "steps"

headers_default = ""
ok_exit_code_default = 0
ok_reason_default = 0
err_request_exit_code_default = 1
err_request_reason_default = 100
err_status_code_exit_code_default = 1
err_status_code_reason_default = 100
err_headers_exit_code_default = 1
err_headers_reason_default = 100
err_body_exit_code_default = 1
err_body_reason_default = 100
method_default = "get"

variable_name_regex = "[a-zA-Z][a-zA-Z0-9]*"

-- configuration items' names
headers_cfg = "headers"
ok_exit_code_cfg = "OK exit code"
ok_reason_cfg = "OK reason"
err_request_exit_code_cfg = "Err request exit code"
err_request_reason_cfg = "Err request reason"
err_status_code_exit_code_cfg = "Err status code exit code"
err_status_code_reason_cfg = "Err status code reason"
err_headers_exit_code_cfg = "Err headers exit code"
err_headers_reason_cfg = "Err headers reason"
err_body_exit_code_cfg = "Err body exit code"
err_body_reason_cfg = "Err body reason"
metric_cfg = "metric"
type_cfg = "type"
url_cfg = "url"
method_cfg = "method"
data_cfg = "data"
status_code_test_cfg = "status code test"
headers_variables_cfg = "headers variables"
body_variables_cfg = "body variables"
headers_test_cfg = "headers test"
body_test_cfg = "body test"
and_cfg = "and"
or_cfg = "or"
not_cfg = "not"
name_cfg = "name"
header_cfg = "header"
filter_cfg = "filter"
path_cfg = "path"
filter_type_cfg = "filter type"
additional_values_cfg = "additional values"
value_cfg = "value"
unit_cfg = "unit"
debug_cfg = "debug"


-- functions ----------------------------------

-- the function checks if file exists

function file_exists(file)
  local f = io.open(file, "r")
  if f then f:close() end
  return f ~= nil
end


-- this function replaces $variable name$ with the variable value
-- Uses: variables

function replace_variables(s)
  if s ~= nil then
    local var = re.match(s,  "\\$(" .. variable_name_regex .. ")\\$")
    while var ~= nil do
      local repl = variables[var]
      if repl == nil then
        repl = ""
      end
      s = re.gsub(s, "\\$" .. var .. "\\$", repl)
      var = re.match(s,  "\\$(" .. variable_name_regex .. ")\\$")
    end
  end
  return s
end


-- this function replaces %code%, %headers% a %body% with the corresponding values
-- Uses: response

function replace_response(s)
  if s ~= nil then
    s = re.gsub(s, "%code%", tostring(response.status_code))
    local headers = ""
    for i=1,#response.headers do
      headers = headers .. response.headers[i] .. "\n"
    end
    s = re.gsub(s, "%headers%", headers)
    s = re.gsub(s, "%body%", response.body)
  end
  return s
end


-- this function extracts object form received headers
-- Uses: response.headers

function extract_from_headers(obj_cfg)
  local object = {}
  local not_found = true

  local header = obj_cfg[header_cfg]
  if header == nil then
    return nil
  end
  header = replace_variables(header)

  for key,value in pairs(response.headers) do
    if re.match(key, header) ~= nil then
      not_found = false
      table.insert(object, value)
    end
  end
  if not_found then
    -- Header not found in the response
    return nil
  end

  return object
end


-- this function extracts object form received body
-- Uses: response.body

function extract_from_body(obj_cfg)
  local object = nil
  local body_type = obj_cfg[type_cfg]
  local body_path = obj_cfg[path_cfg]
  body_path = replace_variables(body_path)

  if body_type == "json" and body_path ~= nil and body_path ~= "" then
    -- find the object at path
    object = jsonpath.find(body_path, response.body)

  elseif  body_type == "xml" and body_path ~= nil and body_path ~= "" then
    -- decode the body as XML
    local xml_object = xmlpath.loadxml(response.body)
    if xml_object == nil then
      -- body is not valid XML
      return nil
    end
    -- compile XPath
    local xml_path = xmlpath.compile(body_path)
    if xml_path == nil then
      -- path is invalid XPath
      return nil
    end

    -- iterate XPath
    local it = xml_path:iter(xml_object)
    local not_found = true
    object = {}
    for key,value in pairs(it) do
      not_found = false
      table.insert(object, value:string())
    end
    if not_found then
      -- XPath not found in the response
      return nil
    end

  else -- body_type == "text" or any other value
    body_type = "text"
    object = response.body
  end

  return object
end


-- this function sets variables from received headers or body
-- Uses: err_......

function set_variables(vars, vars_type)
  if type(vars) ~= "table" then
    if vars_type == "body" then
      amon.value(reason_metric, err_body_reason)
      amon.exit(err_body_exit_code,"Invalid body variables configuration for metric '" .. metric .. "'! Variables configuration is not a table.")
    else
      amon.value(reason_metric, err_headers_reason)
      amon.exit(err_headers_exit_code,"Invalid headers variables configuration for metric '" .. metric .. "'! Variables configuration is not a table.")
    end
  end

  for _,onevar in pairs(vars) do
    if type(onevar) ~= "table" then
      if vars_type == "body" then
        amon.value(reason_metric, err_body_reason)
        amon.exit(err_body_exit_code,"Invalid body variables configuration for metric '" .. metric .. "'! Configuration for some variable is not a table.")
      else
        amon.value(reason_metric, err_headers_reason)
        amon.exit(err_headers_exit_code,"Invalid headers variables configuration for metric '" .. metric .. "'! Configuration for some variable is not a table.")
      end
    end

    local wrong_key
    for key, value in pairs(onevar) do
      if vars_type == "body" and key ~= name_cfg and key ~= type_cfg and key ~= path_cfg and key ~= filter_cfg then
        wrong_key = key
      elseif vars_type ~= "body" and key ~= name_cfg and key ~= header_cfg and key ~= filter_cfg then
        wrong_key = key
      end
    end

    if wrong_key ~= nil then
      if vars_type == "body" then
        amon.value(reason_metric, err_body_reason)
        amon.exit(err_body_exit_code,"Invalid body variables configuration for metric '" .. metric .. "'! Invalid variables item '" .. wrong_key .. "'.")
      else
        amon.value(reason_metric, err_headers_reason)
        amon.exit(err_headers_exit_code,"Invalid headers variables configuration for metric '" .. metric .. "'! Invalid variables item '" .. wrong_key .. "'.")
      end
    end

    if onevar[name_cfg] == nil then
      if vars_type == "body" then
        amon.value(reason_metric, err_body_reason)
        amon.exit(err_body_exit_code,"Invalid body variables configuration for metric '" .. metric .. "'! Variable name is missing.")
      else
        amon.value(reason_metric, err_headers_reason)
        amon.exit(err_headers_exit_code,"Invalid headers variables configuration for metric '" .. metric .. "'! Variable name is missing.")
      end
    end

    local var_name = onevar[name_cfg]
    if re.match(var_name, "^" .. variable_name_regex .. "$") == nil then
      if vars_type == "body" then
        amon.value(reason_metric, err_body_reason)
        amon.exit(err_body_exit_code,"Invalid body variables configuration for metric '" .. metric .. "'! Invalid variable name '" .. var_name .. "'.")
      else
        amon.value(reason_metric, err_headers_reason)
        amon.exit(err_headers_exit_code,"Invalid headers variables configuration for metric '" .. metric .. "'! Invalid variable name '" .. var_name .. "'.")
      end
    end

    -- select object
    local object

    if vars_type == "body" then
      object = extract_from_body(onevar)
    else -- tree_type == "headers"
      object = extract_from_headers(onevar)
    end

    -- find value in the object
    local object_filter = onevar[filter_cfg]
    object_filter = replace_variables(object_filter)
    local new_value


    if object ~= nil then
      if type(object) == "table" then
        for key, value in pairs(object) do
          if object_filter == nil then
            new_value = object[key]
          else
            new_value = re.match(object[key], object_filter)
          end
          if  new_value ~= nil then
            variables[var_name] = new_value
            break
          end
        end
      else
        if object_filter == nil then
          new_value = object
        else
          new_value = re.match(object, object_filter)
        end
        if  new_value ~= nil then
          variables[var_name] = new_value
        end
      end
    end

  end
end


-- this function tests the tree condition for headers or body
-- Uses: err_......
--       metric

function test_tree(condition, tree_type)
  if type(condition) ~= "table" then
    if tree_type == "body" then
      amon.value(reason_metric, err_body_reason)
      amon.exit(err_body_exit_code,"Invalid test condition for body for metric '" .. metric .. "'! Condition is not a table.")
    else
      amon.value(reason_metric, err_headers_reason)
      amon.exit(err_headers_exit_code,"Invalid test condition for headers for metric '" .. metric .. "'! Condition is not a table.")
    end
  end

  local cnt = 0
  local oper
  local wrong_key
  for key, value in pairs(condition) do
    if key == "and" or key == "or" or key == "not" then
      oper = key
    elseif tree_type == "body" and key ~= type_cfg and key ~= path_cfg and key ~= filter_type_cfg and key ~= filter_cfg then
      wrong_key = key
    elseif tree_type ~= "body" and key ~= header_cfg and key ~= filter_type_cfg and key ~= filter_cfg then
      wrong_key = key
    end
    cnt = cnt + 1
  end

  if cnt ~= 1 and oper ~= nil and type(condition[oper]) ~= "table" then
    if tree_type == "body" then
      amon.value(reason_metric, err_body_reason)
      amon.exit(err_body_exit_code,"Invalid body test condition for metric '" .. metric .. "'! Invalid usage of operation '" .. oper .. "'.")
    else
      amon.value(reason_metric, err_headers_reason)
      amon.exit(err_headers_exit_code,"Invalid headers test condition for metric '" .. metric .. "'! Invalid usage of operation '" .. oper .. "'.")
    end
  end

  if oper == nil and wrong_key ~= nil then
    if tree_type == "body" then
      amon.value(reason_metric, err_body_reason)
      amon.exit(err_body_exit_code,"Invalid body test condition for metric '" .. metric .. "'! Invalid test item '" .. wrong_key .. "'.")
    else
      amon.value(reason_metric, err_headers_reason)
      amon.exit(err_headers_exit_code,"Invalid headers test condition for metric '" .. metric .. "'! Invalid test item '" .. wrong_key .. "'.")
    end
  end

  -- processing and condition
  if oper == "and" then
    local result = true
    for _, value in pairs(condition[oper]) do
      if not test_tree(value, tree_type) then
        result = false
      end
    end
    return result

  -- processing or condition
  elseif oper == "or" then
    local result = false
    for _, value in pairs(condition[oper]) do
      if test_tree(value, tree_type) then
        result = true
      end
    end
    return result

  -- processing not condition
  elseif oper == "not" then
    return not test_tree(condition[oper], tree_type)
  end

  -- processing one condition
  -- select object
  local object

  if tree_type == "body" then
    object = extract_from_body(condition)
    if object == nil then
      return false
    end
  else -- tree_type == "headers"
    object = extract_from_headers(condition)
    if object == nil then
      return false
    end
  end

  -- find filter in the object
  local object_filter_type = condition[filter_type_cfg]
  local object_filter = condition[filter_cfg]
  object_filter = replace_variables(object_filter)

  if object_filter ~= nil and object_filter ~= "" then
    if type(object) == "table" then
      local result = false
      for key, value in pairs(object) do
        if object_filter_type == "regex" then
          if re.match(object[key], object_filter) ~= nil then
            result = true
            break
          end
        else -- object_filter_type == "substring" or any other value
          if string.find(object[key], object_filter, 1, true) ~= nil then
            result = true
            break
          end
        end
      end
      return result
    else
      if object_filter_type == "regex" then
        return re.match(object, object_filter) ~= nil
      else -- object_filter_type == "substring" or any other value
        return string.find(object, object_filter, 1, true) ~= nil
      end
    end
  end

  return true
end


-- this function replaces paranetr variables in one include line

function replace_include_parameters(s, p)
  for i=1,table.getn(p) do
    s = re.gsub(s, "%" .. i .. "%", p[i])
   end

  return s
end


-- this function reads one include

function process_include(ln, n)
  -- discard empty lines and comments
  if ln == '' or ln:sub(1, 1) == "#" then
      return "", ""
  end

  -- create line tokens
  tokens={}
  idx = 0
  in_token = false
  quoted = false
  check_next = false
  t = ''
  for i=1,ln:len() do
    c = ln:sub(i,i)
    if in_token then
      if check_next then
        check_next = false
        if c ~= ' ' and c ~= '"' then
          return "", list_fname .. ':' .. n .. ':' .. i .. ' " is not duobled!'
        end
        if c == ' ' then
          in_token = false
          tokens[idx] = t
          idx = idx + 1
          t = ""
        else
          t = t .. c
        end
      else -- NOT check_next
        if quoted then
          if c == '"' then
            check_next = true
          else
            t = t .. c
          end
        else -- NOT quoted
          if c == ' ' then
            in_token = false
            tokens[idx] = t
            idx = idx + 1
            t = ""
          else
            t = t .. c
          end
        end
      end
    else -- NOT in_token
      if c ~= ' ' then
        in_token = true
        if c == '"' then
          quoted = true
        else
          quoted = false
          t = t .. c
        end
      end
    end
  end
  if in_token then
    if quoted then
      return "", list_fname .. ':' .. n .. ' misssing end "!'
    else
      tokens[idx] = t
    end
  end

  -- check if the include file exists
  if not file_exists(tokens[0]) then
    return "", "Include file '" .. tokens[0] .. "' not found!"
  end

  -- read the include file
  incl_file = ""
  for line in io.lines(tokens[0]) do
    incl_file = incl_file .. replace_include_parameters(line, tokens) .. '\n'
  end

  return incl_file, ""
end

-- main program ----------------------------------
cfg_file = ""
cfg_generated = false

-- check if the list file exists
if not file_exists(list_fname) then
  -- check if the configuration file exists
  if not file_exists(cfg_fname) then
    amon.value(reason_metric, err_cfg_reason)
    amon.exit(err_cfg_code, "Configuration file '" .. cfg_fname .. "' not found!")
  end

  -- read the configuration file
  for line in io.lines(cfg_fname) do
    cfg_file = cfg_file .. line .. '\n'
  end
else
  cfg_generated = true
  -- read the list file
  n = 0
  for line in io.lines(list_fname) do
    n = n + 1
    part, emsg = process_include(line, n)
    if emsg ~= "" then
      amon.value(reason_metric, err_cfg_reason)
      amon.exit(err_cfg_code, emsg)
    end

    cfg_file = cfg_file .. part
  end
end

-- parse cfg file
cfg = yaml.parse(cfg_file)
if cfg == nil then
  amon.value(reason_metric, err_cfg_reason)
  if cfg_generated then
    amon.exit(err_cfg_code, "Syntax error in configuration generated from '" .. list_fname .. "'!")
  else
    amon.exit(err_cfg_code, "Syntax error in configuration file '" .. cfg_fname .. "'!")
  end
end

-- set default values from configuration file
defaults = cfg[defaults_cfg]
if defaults ~= nil then
  if defaults[headers_cfg] ~= nil then
    headers_default = defaults[headers_cfg]
  end

  if defaults[ok_exit_code_cfg] ~= nil then
    ok_exit_code_default = defaults[ok_exit_code_cfg]
  end

  if defaults[ok_reason_cfg] ~= nil then
    ok_reason_default = defaults[ok_reason_cfg]
  end

  if defaults[err_request_exit_code_cfg] ~= nil then
    err_request_exit_code_default = defaults[err_request_exit_code_cfg]
  end

  if defaults[err_request_reason_cfg] ~= nil then
    err_request_reason_default = defaults[err_request_reason_cfg]
  end

  if defaults[err_status_code_exit_code_cfg] ~= nil then
    err_status_code_exit_code_default = defaults[err_status_code_exit_code_cfg]
  end

  if defaults[err_status_code_reason_cfg] ~= nil then
    err_status_code_reason_default = defaults[err_status_code_reason_cfg]
  end

  if defaults[err_headers_exit_code_cfg] ~= nil then
    err_headers_exit_code_default = defaults[err_headers_exit_code_cfg]
  end

  if defaults[err_headers_reason_cfg] ~= nil then
    err_headers_reason_default = defaults[err_headers_reason_cfg]
  end

  if defaults[err_body_exit_code_cfg] ~= nil then
    err_body_exit_code_default = defaults[err_body_exit_code_cfg]
  end

  if defaults[err_body_reason_cfg] ~= nil then
    err_body_reason_default = defaults[err_body_reason_cfg]
  end
end


-- variables from configuration
variables = cfg[variables_cfg]
if variables == nil then
  variables = {}
end

for key,value in pairs(variables) do
  if re.match(key, "^" .. variable_name_regex .. "$") == nil then
    amon.value(reason_metric, err_cfg_reason)
    amon.exit(err_cfg_code, "Invalid intial variable name '" .. key .. "'!")
  end
end

-- process all steps
if cfg[steps_cfg] == nil then
  amon.value(reason_metric, err_cfg_reason)
  amon.exit(err_cfg_code, "Missing '" .. steps_cfg .. "' configuration in the configuration file!")
end

-- start time should be read for the first step
read_start_time = true

for k,item in pairs(cfg[steps_cfg]) do
  -- set request patameters from configuration file
  metric = item[metric_cfg]
  if metric == nil or metric == "" then
    amon.value(reason_metric, err_cfg_reason)
    amon.exit(err_cfg_code, "Missing '" .. metric_cfg .. "' in step " .. k .. "!")
  end

  metric_type = item[type_cfg]

  url = item[url_cfg]
  if url == nil or url == "" then
    amon.value(reason_metric, err_cfg_reason)
    amon.exit(err_cfg_code, "Missing '" .. url_cfg .. "' for metric '" .. metric .. "'!")
  end
  url = replace_variables(url)

  method = item[method_cfg]
  if method == nil or method == "" then
    method = method_default
  end

  data = item[data_cfg]
  data = replace_variables(data)


  headers = headers_default
  if item[headers_cfg] ~= nil then
    headers = item[headers_cfg]
  end
  for hdr, val in pairs(headers) do
    headers[hdr] = replace_variables(val)
  end

  err_request_exit_code = err_request_exit_code_default
  if item[err_request_exit_code_cfg] ~= nil then
    err_request_exit_code = item[err_request_exit_code_cfg]
  end

  err_request_reason = err_request_reason_default
  if item[err_request_reason_cfg] ~= nil then
    err_request_reason = item[err_request_reason_cfg]
  end

  err_status_code_exit_code = err_status_code_exit_code_default
  if item[err_status_code_exit_code_cfg] ~= nil then
    err_status_code_exit_code = item[err_status_code_exit_code_cfg]
  end

  err_status_code_reason = err_status_code_reason_default
  if item[err_status_code_reason_cfg] ~= nil then
    err_status_code_reason = item[err_status_code_reason_cfg]
  end

  err_headers_exit_code = err_headers_exit_code_default
  if item[err_headers_exit_code_cfg] ~= nil then
    err_headers_exit_code = item[err_headers_exit_code_cfg]
  end

  err_headers_reason = err_headers_reason_default
  if item[err_headers_reason_cfg] ~= nil then
    err_headers_reason = item[err_headers_reason_cfg]
  end

  err_body_exit_code = err_body_exit_code_default
  if item[err_body_exit_code_cfg] ~= nil then
    err_body_exit_code = item[err_body_exit_code_cfg]
  end

  err_body_reason = err_body_reason_default
  if item[err_body_reason_cfg] ~= nil then
    err_body_reason = item[err_body_reason_cfg]
  end

  -- read start time
  if read_start_time and metric_type ~= "ignore" then
    start_time = time.now()
  end

  -- for join don't reead start time in the next step
  read_start_time =  metric_type ~= "join"

  -- process request
  response, error_message = http.request(method, url,  {headers=headers, body=data})

  -- calculate step time
  if metric_type ~= "ignore" and  metric_type ~= "join" then
    end_time = time.now()
    step_time = end_time:sub(start_time)
  end

  if response == nil then
    -- request failed
    amon.value(reason_metric, err_request_reason_default)
    amon.exit(err_request_exit_code_default, error_message)
  end


  -- status code processing
  status_code_test = item[status_code_test_cfg]

  if status_code_test ~= nil then
    -- check status code
    if status_code_test ~= response.status_code then
      amon.value(reason_metric, err_status_code_reason)
      amon.exit(err_status_code_exit_code,"Status code for metric '" .. metric .. "': " .. response.status_code .. " doesn't match expected value " .. status_code_test .. "!")
    end
  end

  -- headers variables processing
  headers_variables = item[headers_variables_cfg]
  if  headers_variables ~= nil then
    set_variables(headers_variables, "headers")
  end

  -- body variables processing
  body_variables = item[body_variables_cfg]
  if  body_variables ~= nil then
    set_variables(body_variables, "body")
  end

  -- write log
  if type(item[debug_cfg]) == "table" then
    for l,logitem in pairs(item[debug_cfg]) do
      if type(logitem) == "string" then
        logtxt = replace_variables(logitem)
        logtxt = replace_response(logtxt)
        print(logtxt)
      else
        print("Invalid ".. debug_cfg .. " configuration!")
      end
    end
  end

  -- headers test processing
  headers_test = item[headers_test_cfg]
  if  headers_test ~= nil then
    if not test_tree(headers_test, "headers") then
      amon.value(reason_metric, err_headers_reason)
      amon.exit(err_headers_exit_code,"Headers condition for metric '" .. metric .. "' not met!")
    end
  end

  -- body test processing
  body_test = item[body_test_cfg]
  if  body_test ~= nil then
    if not test_tree(body_test, "body") then
      amon.value(reason_metric, err_body_reason)
      amon.exit(err_body_exit_code,"Body condition for metric '" .. metric .. "' not met!")
    end
  end

  -- write metric value (step time)
  if metric_type ~= "ignore" and  metric_type ~= "join" then
    amon.value(metric, step_time, "s")
  end


  -- write additional_values
  if type(item[additional_values_cfg]) == "table" then
    for v, val in pairs(item[additional_values_cfg]) do
      val_name = replace_variables(val[name_cfg])
      if type(val[value_cfg]) == "string" then
        val_value = replace_variables(val[value_cfg])
      else
        val_value = replace_variables(tostring(val[value_cfg]))
      end
      val_value = tonumber(replace_response(val_value))
      val_unit = replace_variables(val[unit_cfg])
      if val_name ~= nil and val_value ~= nil then
        if val_name ~= nil then
          amon.value(val_name,val_value, val_unit)
        else
          amon.value(val_name, val_value)
        end
      end
    end
  end

end

-- everything was OK
amon.value(reason_metric, ok_reason_default)
amon.exit(ok_exit_code_default, "OK")



