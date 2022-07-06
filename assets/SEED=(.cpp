void __cdecl FUN_0070a120(int param_1)

{
  uint uVar1;
  int **ppiVar2;
  void *pvVar3;
  int iVar4;
  int iVar5;
  undefined extraout_DL;
  undefined extraout_DL_00;
  undefined extraout_DL_01;
  undefined extraout_DL_02;
  undefined extraout_DL_03;
  undefined uVar6;
  int **in_FS_OFFSET;
  char **ppcVar7;
  char *pcVar8;
  float *pfVar9;
  int *piVar10;
  char *pcVar11;
  char *pcVar12;
  char *pcVar13;
  undefined in_stack_ffffff0c;
  float fStack192;
  int iStack188;
  char *local_b8;
  void *apvStack180 [5];
  uint uStack160;
  void *apvStack156 [6];
  uint local_84;
  int *local_4c;
  undefined *puStack72;
  undefined4 uStack68;
  
  uStack68 = 0xffffffff;
  puStack72 = &LAB_00c97be0;
  local_4c = *in_FS_OFFSET;
  local_84 = DAT_00f3a000 ^ (uint)&stack0xffffff0c;
  uVar1 = DAT_00f3a000 ^ (uint)&stack0xffffff00;
  *in_FS_OFFSET = (int *)&local_4c;
  local_b8 = 
  "Random( a:int = optional, b:int = optional ) -> number|int. [This is kinda messy. If given 0 argu ments, returns number between 0.0 and 1.0. If given 1 arguments, returns int between 0 and \'a\'.  If given 2 arguments returns int between \'a\' and \'b\'.]"
  ;
  iStack188 = lua_gettop();
  
  if (iStack188 == 0) {
    iVar5 = (int)_DAT_0100bbb8 * 0x41a7 + ((int)_DAT_0100bbb8 / 0x1f31d) * -0x7fffffff;
    if (iVar5 < 1) {
      iVar5 = iVar5 + 0x7fffffff;
    }
    fStack192 = (float)iVar5 * 4.656613e-10;
    lua_checkstack(param_1,1);
    lua_pushnumber(param_1,(double)fStack192);
    uVar6 = extraout_DL_01;
  }
  else {
    if (iStack188 == 1) {
      iVar5 = lua_tointeger(param_1,1,uVar1);
      iVar4 = 0;
    }
    else {
      fStack192 = (float)lua_gettop();
      
      iVar4 = lua_tointeger(param_1,1,uVar1);
      iVar5 = lua_tointeger(param_1,2);
    }
    iVar5 = FUN_0046f390(&DAT_0100bbb8,iVar4,iVar5);
    lua_checkstack(param_1,1);
    lua_pushinteger(param_1,iVar5);
    uVar6 = extraout_DL_03;
  }
LAB_0070a3ca:
  *in_FS_OFFSET = local_4c;
  FUN_00c5beba(local_84 ^ (uint)&stack0xffffff0c,uVar6,in_stack_ffffff0c);
  return;
}