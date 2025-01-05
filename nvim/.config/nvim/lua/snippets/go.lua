local ls = require 'luasnip'
local s = ls.snippet
local i = ls.insert_node
local fmt = require('luasnip.extras.fmt').fmt
local rep = require('luasnip.extras').rep

return {
  -- Your existing error snippet
  s(
    {
      trig = 'iferr',
      name = 'Error check',
      dscr = 'Snippet for error checking',
    },
    fmt(
      [[
if {} != nil {{
    return fmt.Errorf("{}: %w", {})
}}
      ]],
      {
        i(1, 'err'),
        i(2, 'context'),
        rep(1),
      }
    )
  ),

  -- New test snippet
  s(
    {
      trig = 'gotest',
      name = 'Test function',
      dscr = 'Create a new test function',
    },
    fmt(
      [[
func Test{}(t *testing.T) {{
    tests := []struct {{
        name    string
        {} {}
        want    {}
    }}{{
        {{
            name: "{}",
            {}: {},
            want: {},
        }},
    }}

    for _, tt := range tests {{
        t.Run(tt.name, func(t *testing.T) {{
            got := {}({})
            if got != tt.want {{
                t.Errorf("{} = %v, want %v", got, tt.want)
            }}
        }})
    }}
}}
      ]],
      {
        i(1, 'Name'), -- Test function name
        i(2, 'input'), -- Input field name
        i(3, 'string'), -- Input type
        i(4, 'string'), -- Output type
        i(5, 'basic test'), -- Test case name
        rep(2), -- Repeat input field name
        i(6, '""'), -- Input value
        i(7, '""'), -- Expected output
        i(8, 'functionName'), -- Function being tested
        rep(2), -- Repeat input field name
        rep(8), -- Repeat function name
      }
    )
  ),
}
