local M = {}

function M.setup()
  -- Clear existing highlights
  vim.cmd 'highlight clear'
  if vim.fn.exists 'syntax_on' then
    vim.cmd 'syntax reset'
  end

  -- Set the color scheme name
  vim.g.colors_name = 'polar'

  -- Enable 24-bit RGB color in the TUI
  vim.opt.termguicolors = true

  -- Define your color palette
  local colors = {
    black = '#000000',
    darkGray = '#222222',
    midgray = '#555555',
    white = '#ffffff',
    dawnPink = '#ffb3b3',
    sky = '#00eeee',
    river = '#005ccc',
    deepBlue = '#0000dd',
    ocean = '#18005e',
    navy = '#0D0427',
    engineSmoke = '#020226',
    candle = '#ff9c00',
    purple = '#aa00aa',
    codeRed = '#ff0000',
    codeYellow = '#ffff00',
  }

  -- Set highlight groups
  local highlights = {
    -- Basic Syntax
    Normal = { fg = colors.sky },
    Comment = { fg = colors.midgray, italic = true },
    String = { fg = colors.white },
    -- Character = { fg = colors.white },
    -- Number = { fg = colors.sky },
    -- Boolean = { fg = colors.sky },
    -- Float = { fg = colors.sky },
    -- Identifier = { fg = colors.fg },
    Function = { fg = colors.sky },
    -- Statement = { fg = colors.sky },
    -- Conditional = { fg = colors.sky },
    -- Repeat = { fg = colors.sky },
    -- Label = { fg = colors.sky },
    Operator = { fg = colors.sky },
    Keyword = { fg = colors.dawnPink, bold = true },
    -- Exception = { fg = colors.sky },
    -- PreProc = { fg = colors.sky },
    -- Include = { fg = colors.sky },
    -- Define = { fg = colors.sky },
    -- Macro = { fg = colors.sky },
    -- PreCondit = { fg = colors.sky },
    -- Type = { fg = colors.sky },
    -- StorageClass = { fg = colors.sky },
    -- Structure = { fg = colors.sky },
    -- Typedef = { fg = colors.sky },
    Special = { fg = colors.sky },
    -- SpecialChar = { fg = colors.candle },
    Tag = { fg = colors.candle },
    Delimiter = { fg = colors.candle },
    -- SpecialComment = { fg = colors.midgray },
    -- Debug = { fg = colors.codeRed },
    -- Underlined = { underline = true },
    -- Ignore = { },
    Error = { fg = colors.codeRed },
    -- Todo = { fg = colors.sky, bold = true },

    -- Editor UI
    Cursor = {bg = colors.candle, fg = colors.black },
    CursorLine = { bg = colors.engineSmoke, fg = colors.candle },
    -- CursorColumn = { bg = colors.sky },
    -- ColorColumn = { bg = colors.navy },
    -- Conceal = { },
    LineNr = { fg = colors.midgray },
    CursorLineNr = { fg = colors.candle },
    -- SignColumn = { },
    -- VertSplit = { fg = colors.midgray },
    -- Folded = { fg = colors.midgray, bg = colors.navy },
    -- FoldColumn = { },
    -- MatchParen = { bg = colors.midgray },
    -- NonText = { fg = colors.midgray },
    Pmenu = { fg = colors.sky, bg = colors.midgray },
    PmenuSel = { fg = colors.candle, bg = colors.midgray },
    -- PmenuSbar = { bg = colors.navy },
    -- PmenuThumb = { bg = colors.sky },
    -- Question = { fg = colors.sky },
    Search = { fg = colors.navy, bg = colors.sky },
    IncSearch = { fg = colors.navy, bg = colors.dawnPink },
    -- SpecialKey = { fg = colors.midgray },
    -- SpellBad = { undercurl = true, sp = colors.codeRed },
    -- SpellCap = { undercurl = true, sp = colors.codeYellow },
    -- SpellLocal = { undercurl = true, sp = colors.sky },
    -- SpellRare = { undercurl = true, sp = colors.candle },
    StatusLine = { fg = colors.sky, bg = colors.midgray },
    StatusLineNC = { fg = colors.sky, bg = colors.midgray },
    -- TabLine = { fg = colors.midgray, bg = colors.navy },
    -- TabLineFill = { bg = colors.navy },
    -- TabLineSel = { fg = colors.fg, bg = colors.sky },
    -- Title = { fg = colors.sky, bold = true },

    Visual = { bg = colors.darkGray },
    -- VisualNOS = { bg = colors.midgray },
    -- WarningMsg = { fg = colors.codeYellow },
    -- WildMenu = { fg = colors.navy, bg = colors.sky },

    -- Diff
    -- DiffAdd = { fg = colors.green },
    -- DiffChange = { fg = colors.codeYellow },
    -- DiffDelete = { fg = colors.codeRed },
    -- DiffText = { fg = colors.sky },

    -- Diagnostics
    DiagnosticSignError = { fg = colors.codeRed },
    DiagnosticSignWarn = { fg = colors.codeYellow },
    DiagnosticSignInfo = { fg = colors.codeYellow },
    DiagnosticSignHint = { fg = colors.codeYellow },
    DiagnosticVirtualTextError = { fg = colors.codeRed },
    DiagnosticVirtualTextWarn = { fg = colors.codeYellow },
    DiagnosticVirtualTextInfo = { fg = colors.codeYellow },
    DiagnosticVirtualTextHint = { fg = colors.codeYellow },
    -- DiagnosticUnderlineError = { undercurl = true, sp = colors.codeRed },
    -- DiagnosticUnderlineWarn = { undercurl = true, sp = colors.codeYellow },
    -- DiagnosticUnderlineInfo = { undercurl = true, sp = colors.codeYellow },
    -- DiagnosticUnderlineHint = { undercurl = true, sp = colors.codeYellow },

    -- LSP
    NormalFloat = { bg = colors.darkGray },
    -- LspReferenceText = { bg = colors.midgray },
    -- LspReferenceRead = { bg = colors.midgray },
    -- LspReferenceWrite = { bg = colors.midgray },

    -- Treesitter
    ['@constant'] = { fg = colors.sky },
    ['@constant.builtin'] = { fg = colors.sky }, -- for nil, true, false
    ['@constant.macro'] = { fg = colors.sky },
    ['@constant.numeric'] = { fg = colors.sky }, -- for numbers
    -- ['@attribute'] = { fg = colors.candle },
    -- ['@boolean'] = { fg = colors.sky },
    -- ['@character'] = { fg = colors.white },
    -- ['@constructor'] = { fg = colors.sky },
    -- ['@error'] = { fg = colors.codeRed },
    -- ['@exception'] = { fg = colors.codeRed },
    -- ['@field'] = { fg = colors.fg },
    -- ['@float'] = { fg = colors.sky },
    -- ['@function.builtin'] = { fg = colors.sky },
    -- ['@function.macro'] = { fg = colors.sky },
    -- ['@include'] = { fg = colors.sky },
    -- ['@label'] = { fg = colors.candle },
    -- ['@method'] = { fg = colors.sky },
    -- ['@namespace'] = { fg = colors.sky },
    -- ['@operator'] = { fg = colors.candle },
    -- ['@parameter'] = { fg = colors.fg },
    -- ['@property'] = { fg = colors.fg },
    -- ['@punctuation.delimiter'] = { fg = colors.candle },
    ['@punctuation.bracket'] = { fg = colors.candle }, -- This is likely what you meant by 'Bracket'
    -- ['@punctuation.special'] = { fg = colors.candle },
    -- ['@repeat'] = { fg = colors.sky },
    -- ['@string.regex'] = { fg = colors.white },
    -- ['@string.escape'] = { fg = colors.candle },
    -- ['@symbol'] = { fg = colors.candle },
    -- ['@tag'] = { fg = colors.sky },
    -- ['@type'] = { fg = colors.sky },
    -- ['@type.builtin'] = { fg = colors.sky },
    ['@variable'] = { fg = colors.sky, bold = true },
    -- ['@variable.builtin'] = { fg = colors.sky },

    -- Git
    -- GitSignsAdd = { fg = colors.green },
    -- GitSignsChange = { fg = colors.codeYellow },
    -- GitSignsDelete = { fg = colors.codeRed },

    -- Neovim Terminal Colors
    -- Terminal = { },
    -- TermCursor = { fg = colors.sky },
    -- TermCursorNC = { },

    -- status line colors
    MiniStatuslineModeNormal = { fg = colors.navy, bg = colors.sky },
    MiniStatuslineModeInsert = { fg = colors.navy, bg = colors.river },
    MiniStatuslineModeVisual = { fg = colors.navy, bg = colors.candle },
    MiniStatuslineModeReplace = { fg = colors.navy, bg = colors.purple },
    MiniStatuslineModeCommand = { fg = colors.navy, bg = colors.white },
    MiniStatuslineDevinfo = { fg = colors.sky, bg = colors.darkGray },
    MiniStatuslineFilename = { fg = colors.white, bg = colors.darkGray },
    MiniStatuslineFileinfo = { fg = colors.sky, bg = colors.darkGray },
    MiniStatuslineInactive = { fg = colors.midgray, bg = colors.darkGray },

  }
  -- Function to set highlights
  local function set_highlights()
    for group, opts in pairs(highlights) do
      vim.api.nvim_set_hl(0, group, opts)
    end
  end

  -- Set up the colorscheme
  if vim.g.colors_name then
    vim.cmd 'hi clear'
  end

  set_highlights()

  -- Create an autocommand to apply highlights when the colorscheme is loaded
  vim.api.nvim_create_augroup('PolarTheme', { clear = true })
  vim.api.nvim_create_autocmd('ColorScheme', {
    group = 'PolarTheme',
    pattern = 'polar',
    callback = set_highlights,
  })
end

-- Function to load the colorscheme
function M.load()
  if vim.g.colors_name then
    vim.cmd 'hi clear'
  end
  vim.o.termguicolors = true
  vim.g.colors_name = 'polar'
  M.setup()
end

return M
