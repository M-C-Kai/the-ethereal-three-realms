.class public final Lpmsj/work/e/cn;
.super Lpmsj/work/d/c;


# instance fields
.field private K:Z

.field private L:Z

.field private M:[Ljava/lang/String;

.field private final N:I

.field private O:Lpmsj/work/b/n;

.field private P:Lpmsj/work/d/l;

.field private final Q:B

.field private final R:B

.field private final S:B

.field private final T:B

.field private U:[Lpmsj/work/a/b;

.field private V:Lpmsj/work/a/i;

.field private W:Lpmsj/work/a/i;

.field private X:Lpmsj/work/a/i;

.field private Y:Lpmsj/work/a/i;

.field private Z:Lpmsj/work/a/i;

.field private final a:I

.field private aa:Lpmsj/work/a/i;

.field private final ab:I

.field private final ac:B

.field private ad:Ljava/lang/StringBuffer;

.field private final b:I

.field private c:Lpmsj/work/d/g;

.field private d:Z

.field private e:Ljava/util/Vector;

.field private f:I


# direct methods
.method public constructor <init>()V
    .locals 6

    const v5, 0x24a0fa

    const v4, 0x24a096

    const/4 v3, 0x2

    const/4 v2, 0x1

    const/4 v1, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const v0, 0xb79b

    iput v0, p0, Lpmsj/work/e/cn;->a:I

    const v0, 0xb799

    iput v0, p0, Lpmsj/work/e/cn;->b:I

    iput-boolean v1, p0, Lpmsj/work/e/cn;->d:Z

    const/16 v0, 0x54

    iput v0, p0, Lpmsj/work/e/cn;->N:I

    iput-byte v1, p0, Lpmsj/work/e/cn;->Q:B

    iput-byte v2, p0, Lpmsj/work/e/cn;->R:B

    iput-byte v3, p0, Lpmsj/work/e/cn;->S:B

    iput-byte v1, p0, Lpmsj/work/e/cn;->T:B

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v5, v1}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->V:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v5, v2}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->W:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v5, v3}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->X:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v4, v1}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->Y:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v4, v2}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->Z:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v4, v3}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/e/cn;->aa:Lpmsj/work/a/i;

    const/16 v0, 0xa0

    iput v0, p0, Lpmsj/work/e/cn;->ab:I

    const/16 v0, 0xa

    iput-byte v0, p0, Lpmsj/work/e/cn;->ac:B

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    iput-object v0, p0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    return-void
.end method


# virtual methods
.method public final a(Ljava/util/Vector;[Ljava/lang/String;IZZZ)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iput-object p2, p0, Lpmsj/work/e/cn;->M:[Ljava/lang/String;

    iput p3, p0, Lpmsj/work/e/cn;->f:I

    iput-boolean p4, p0, Lpmsj/work/e/cn;->K:Z

    iput-boolean p5, p0, Lpmsj/work/e/cn;->L:Z

    iput-boolean p6, p0, Lpmsj/work/e/cn;->d:Z

    invoke-virtual {p0}, Lpmsj/work/e/cn;->ag()V

    return-void
.end method

.method public final a(ILjava/lang/String;)Z
    .locals 10

    const/4 v5, 0x2

    const/4 v3, 0x0

    const/4 v9, 0x1

    iget-object v1, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iget-object v2, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v2}, Lpmsj/work/d/g;->g()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    move-object v0, v1

    check-cast v0, Lpmsj/work/b/u;

    move-object v4, v0

    if-nez p1, :cond_2

    const-string v1, ""

    invoke-virtual {p2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_0

    move v1, v3

    :goto_0
    return v1

    :cond_0
    const/16 v1, 0x46a

    new-instance v2, La/c/h;

    const/16 v3, 0xf

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    invoke-virtual {v4}, Lpmsj/work/b/u;->u()I

    move-result v4

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/p;

    invoke-direct {v4, p2}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static {v1, v2, v3, v4}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;)V

    :cond_1
    :goto_1
    move v1, v9

    goto :goto_0

    :cond_2
    if-eq v9, p1, :cond_3

    if-ne v5, p1, :cond_1

    :cond_3
    invoke-virtual {p2}, Ljava/lang/String;->length()I

    move-result v1

    if-nez v1, :cond_4

    move v1, v3

    goto :goto_0

    :cond_4
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v8

    if-ne v9, p1, :cond_6

    const/16 v1, 0x472

    new-instance v2, La/c/h;

    const/16 v3, 0x9

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    invoke-virtual {v4}, Lpmsj/work/b/u;->u()I

    move-result v4

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/h;

    const/4 v5, 0x3

    invoke-direct {v4, v5}, La/c/h;-><init>(B)V

    new-instance v5, La/c/m;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v6

    invoke-virtual {v6}, Lpmsj/work/b/m;->h()I

    move-result v6

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/h;

    invoke-direct {v6, v9}, La/c/h;-><init>(B)V

    new-instance v7, La/c/m;

    invoke-direct {v7, v8}, La/c/m;-><init>(I)V

    invoke-static/range {v1 .. v7}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    :cond_5
    :goto_2
    invoke-virtual {p0}, Lpmsj/work/e/cn;->ae()V

    goto :goto_1

    :cond_6
    if-ne v5, p1, :cond_5

    const/16 v1, 0x6c3

    const/4 v2, 0x5

    invoke-virtual {v4}, Lpmsj/work/b/u;->u()I

    move-result v3

    invoke-static {v1, v2, v3, v8, v9}, Lpmsj/work/main/w;->a(IBIIB)V

    goto :goto_2
.end method

.method public final ag()V
    .locals 21

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v5

    const/16 v6, 0x20

    invoke-virtual {v5, v6}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v5

    check-cast v5, Lpmsj/work/e/ei;

    if-eqz v5, :cond_0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/e/cn;->I:I

    move v6, v0

    const/4 v7, 0x1

    if-ne v6, v7, :cond_0

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/cn;->i()Z

    move-result v6

    if-nez v6, :cond_0

    invoke-virtual {v5}, Lpmsj/work/e/ei;->ae()V

    :cond_0
    new-instance v7, Ljava/lang/StringBuffer;

    invoke-direct {v7}, Ljava/lang/StringBuffer;-><init>()V

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/e/cn;->f:I

    move v5, v0

    if-eqz v5, :cond_4

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/e/cn;->f:I

    move v5, v0

    invoke-static {v5}, Lpmsj/work/b/a;->b(I)Lpmsj/work/b/j;

    move-result-object v5

    if-nez v5, :cond_2

    const-string v5, "\u7269\u54c1\u5df2\u7528\u5b8c"

    move-object/from16 v0, p0

    move-object v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/e/cn;->d(Ljava/lang/String;)V

    :goto_0
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v5

    if-nez v5, :cond_5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    const/4 v6, 0x0

    invoke-virtual {v5, v6}, Lpmsj/work/d/g;->a(Z)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->P:Lpmsj/work/d/l;

    move-object v5, v0

    const/4 v6, 0x0

    invoke-virtual {v5, v6}, Lpmsj/work/d/l;->a(Z)V

    :cond_1
    :goto_1
    return-void

    :cond_2
    const/4 v6, 0x0

    invoke-virtual {v7, v6}, Ljava/lang/StringBuffer;->setLength(I)V

    iget-object v6, v5, Lpmsj/work/b/j;->o:Ljava/lang/String;

    invoke-virtual {v7, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-short v6, v5, Lpmsj/work/b/j;->g:S

    const/4 v8, 0x1

    if-le v6, v8, :cond_3

    const-string v6, ":"

    invoke-virtual {v7, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-short v5, v5, Lpmsj/work/b/j;->g:S

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v5, "\u4e2a"

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_3
    invoke-virtual {v7}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    move-object/from16 v0, p0

    move-object v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/e/cn;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_4
    const/4 v5, 0x0

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->setLength(I)V

    const-string v5, "\u5ba0\u7269\u5217\u8868"

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/b/f;->a()I

    move-result v5

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v5, "/"

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/ab;->m()I

    move-result v5

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    invoke-virtual {v7}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    move-object/from16 v0, p0

    move-object v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/e/cn;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_5
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/d/g;->c()V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v8

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->P:Lpmsj/work/d/l;

    move-object v5, v0

    mul-int/lit8 v6, v8, 0x54

    add-int/lit8 v6, v6, 0xf

    invoke-virtual {v5, v6}, Lpmsj/work/d/l;->j(I)V

    const/4 v5, 0x0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/d/g;->l()I

    move-result v9

    mul-int/2addr v9, v8

    invoke-virtual {v6, v9}, Lpmsj/work/d/g;->c(I)V

    new-instance v9, Lpmsj/work/a/i;

    const v6, 0x227e46

    invoke-direct {v9, v6}, Lpmsj/work/a/i;-><init>(I)V

    new-instance v10, Lpmsj/work/a/i;

    const v6, 0x22803a

    invoke-direct {v10, v6}, Lpmsj/work/a/i;-><init>(I)V

    const/4 v6, 0x2

    new-array v11, v6, [I

    fill-array-data v11, :array_0

    const/4 v6, 0x2

    new-array v12, v6, [I

    fill-array-data v12, :array_1

    const/4 v6, 0x2

    new-array v13, v6, [I

    fill-array-data v13, :array_2

    const/4 v6, 0x0

    move v14, v6

    :goto_2
    if-ge v14, v8, :cond_c

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5, v14}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v6

    check-cast v6, Lpmsj/work/b/n;

    invoke-virtual {v6}, Lpmsj/work/b/n;->F()La/a/d;

    move-result-object v5

    new-instance v15, Lpmsj/work/d/a;

    const-string v16, ""

    const/16 v17, 0x32

    const/16 v18, 0x32

    invoke-direct/range {v15 .. v18}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;II)V

    invoke-virtual {v15, v9, v10}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    const/16 v16, 0x1000

    invoke-virtual/range {v15 .. v16}, Lpmsj/work/d/a;->l(I)V

    invoke-virtual {v15, v5}, Lpmsj/work/d/a;->a(La/a/d;)V

    const/16 v5, -0x12

    invoke-virtual {v15, v5}, Lpmsj/work/d/a;->i(I)V

    move-object/from16 v0, p0

    iget-boolean v0, v0, Lpmsj/work/e/cn;->d:Z

    move v5, v0

    if-eqz v5, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    mul-int/lit8 v16, v14, 0x2

    const/16 v17, 0xa

    const/16 v18, 0xf

    move-object v0, v5

    move-object v1, v15

    move/from16 v2, v16

    move/from16 v3, v17

    move/from16 v4, v18

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;III)V

    :goto_3
    new-instance v16, Lpmsj/work/d/l;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    const/16 v17, 0x1

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->p(I)I

    move-result v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object/from16 v17, v0

    const/16 v18, 0x1

    invoke-virtual/range {v17 .. v18}, Lpmsj/work/d/g;->q(I)I

    move-result v17

    move-object/from16 v0, v16

    move v1, v5

    move/from16 v2, v17

    invoke-direct {v0, v1, v2}, Lpmsj/work/d/l;-><init>(II)V

    invoke-virtual/range {v16 .. v16}, Lpmsj/work/d/l;->R()V

    invoke-virtual {v6}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v5

    const/16 v17, 0x0

    const/16 v18, -0x4

    move-object/from16 v0, v16

    move-object v1, v5

    move/from16 v2, v17

    move/from16 v3, v18

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    const/4 v5, 0x0

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->setLength(I)V

    const-string v5, "*9"

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v6}, Lpmsj/work/b/n;->c()I

    move-result v5

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v5, "\u7ea7"

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v7}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    move-object/from16 v0, v16

    move-object v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/e/cn;->f:I

    move v5, v0

    if-nez v5, :cond_8

    instance-of v5, v6, Lpmsj/work/b/u;

    if-eqz v5, :cond_8

    move-object v0, v6

    check-cast v0, Lpmsj/work/b/u;

    move-object v5, v0

    const/16 v17, 0x0

    move-object v0, v7

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    const-string v17, "*9\u72b6\u6001\uff1a"

    move-object v0, v7

    move-object/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v17, 0xb

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->f(B)I

    move-result v17

    const/16 v18, 0x1

    move/from16 v0, v17

    move/from16 v1, v18

    if-ne v0, v1, :cond_a

    const-string v17, "\u51fa\u6218"

    move-object v0, v7

    move-object/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_4
    const/16 v17, 0xc

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->f(B)I

    move-result v17

    const/16 v18, 0x1

    move/from16 v0, v17

    move/from16 v1, v18

    if-ne v0, v1, :cond_6

    const-string v17, "/"

    move-object v0, v7

    move-object/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v17, "\u6e9c\u5ba0"

    move-object v0, v7

    move-object/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_6
    invoke-virtual {v7}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v17

    const/16 v18, 0x0

    const/16 v19, -0x9

    invoke-virtual/range {v16 .. v19}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    const/16 v17, 0x0

    move-object v0, v7

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    const/16 v17, 0x3c

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->f(B)I

    move-result v17

    const/16 v18, 0x1

    move/from16 v0, v17

    move/from16 v1, v18

    if-ne v0, v1, :cond_b

    const v17, 0x38d0b

    const/16 v18, 0x2

    invoke-static/range {v17 .. v18}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v17

    invoke-virtual/range {v16 .. v17}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    :cond_7
    :goto_5
    const/16 v17, 0x6

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->f(B)I

    move-result v17

    if-lez v17, :cond_8

    const/16 v17, 0x6

    move-object v0, v5

    move/from16 v1, v17

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->f(B)I

    move-result v5

    mul-int/lit8 v5, v5, 0xf

    add-int/lit8 v5, v5, 0x32

    div-int/lit8 v5, v5, 0x64

    const v17, 0x563851

    const/16 v18, 0xf

    const/16 v19, 0x3

    const/16 v20, 0x1

    move/from16 v0, v17

    move v1, v5

    move/from16 v2, v18

    move/from16 v3, v19

    move/from16 v4, v20

    invoke-static {v0, v1, v2, v3, v4}, Lpmsj/work/main/c;->a(IIIIZ)Ljava/lang/String;

    move-result-object v5

    const/16 v17, 0x0

    const/16 v18, -0xd

    move-object/from16 v0, v16

    move-object v1, v5

    move/from16 v2, v17

    move/from16 v3, v18

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/l;->a(Ljava/lang/String;II)Z

    :cond_8
    invoke-virtual {v6}, Lpmsj/work/b/n;->t()I

    move-result v5

    const/16 v6, 0x54

    invoke-static {v5, v6}, Ljava/lang/Math;->max(II)I

    move-result v5

    const/16 v6, 0x32

    invoke-virtual {v15, v6, v5}, Lpmsj/work/d/a;->e(II)V

    move-object/from16 v0, v16

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->j(I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v6, v0

    mul-int/lit8 v15, v14, 0x2

    add-int/lit8 v15, v15, 0x1

    move-object v0, v6

    move-object/from16 v1, v16

    move v2, v15

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v6, v0

    invoke-virtual {v6, v14, v5}, Lpmsj/work/d/g;->h(II)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    invoke-virtual {v5, v11, v12, v13}, Lpmsj/work/d/g;->b([I[I[I)V

    add-int/lit8 v5, v14, 0x1

    move v14, v5

    move-object/from16 v5, v16

    goto/16 :goto_2

    :cond_9
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    mul-int/lit8 v16, v14, 0x2

    const/16 v17, 0x0

    const/16 v18, 0x9

    move-object v0, v5

    move-object v1, v15

    move/from16 v2, v16

    move/from16 v3, v17

    move/from16 v4, v18

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;III)V

    goto/16 :goto_3

    :cond_a
    const-string v17, "\u5f85\u547d"

    move-object v0, v7

    move-object/from16 v1, v17

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto/16 :goto_4

    :cond_b
    if-nez v17, :cond_7

    const v17, 0x38d0b

    const/16 v18, 0x3

    invoke-static/range {v17 .. v18}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v17

    invoke-virtual/range {v16 .. v17}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    goto/16 :goto_5

    :cond_c
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v6, v0

    iget v5, v5, Lpmsj/work/d/b;->k:I

    add-int/lit8 v5, v5, 0x55

    iput v5, v6, Lpmsj/work/d/b;->k:I

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/d/g;->m()V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    const/4 v6, 0x4

    invoke-virtual {v5, v6}, Lpmsj/work/d/g;->l(I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/d/g;->i()Z

    move-result v5

    if-eqz v5, :cond_1

    sget-object v5, Lpmsj/work/a/c;->Z:[S

    const/4 v6, 0x4

    aget-short v5, v5, v6

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/e/cn;->h(I)V

    goto/16 :goto_1

    nop

    :array_0
    .array-data 4
        0xa
        0x0
    .end array-data

    :array_1
    .array-data 4
        -0xa
        0x8
    .end array-data

    :array_2
    .array-data 4
        0x0
        0x1
    .end array-data
.end method

.method protected final b(Lpmsj/work/d/b;)V
    .locals 5

    iget v0, p1, Lpmsj/work/d/b;->g:I

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    iget-object v0, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v0}, Lpmsj/work/d/g;->g()I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-ge v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iget-object v1, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v1}, Lpmsj/work/d/g;->g()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->u()I

    move-result v1

    iget v2, p0, Lpmsj/work/e/cn;->f:I

    if-eqz v2, :cond_2

    iget v0, p0, Lpmsj/work/e/cn;->f:I

    invoke-static {v0}, Lpmsj/work/b/a;->b(I)Lpmsj/work/b/j;

    move-result-object v0

    if-nez v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u7269\u54c1\u5df2\u7528\u5b8c"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    invoke-virtual {p0}, Lpmsj/work/e/cn;->ae()V

    goto :goto_0

    :cond_1
    const/16 v0, 0x3f1

    const/4 v2, 0x4

    iget v3, p0, Lpmsj/work/e/cn;->f:I

    invoke-static {v0, v2, v3, v1}, Lpmsj/work/main/w;->a(ISII)V

    goto :goto_0

    :cond_2
    iget-object v1, p0, Lpmsj/work/e/cn;->M:[Ljava/lang/String;

    if-eqz v1, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/cn;->M:[Ljava/lang/String;

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0

    :cond_3
    iget-boolean v1, p0, Lpmsj/work/e/cn;->L:Z

    if-eqz v1, :cond_7

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    new-instance v2, Ljava/util/Vector;

    const/4 v0, 0x5

    invoke-direct {v2, v0}, Ljava/util/Vector;-><init>(I)V

    iget-object v0, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iget-object v3, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v3}, Lpmsj/work/d/g;->g()I

    move-result v3

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/u;

    const-string v3, "\u5c5e\u6027"

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const/16 v3, 0xb

    invoke-virtual {v0, v3}, Lpmsj/work/b/u;->f(B)I

    move-result v3

    if-nez v3, :cond_5

    const-string v3, "\u51fa\u6218"

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_4
    :goto_1
    const-string v3, "\u6539\u540d"

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v3, "\u653e\u751f"

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const/16 v3, 0xc

    invoke-virtual {v0, v3}, Lpmsj/work/b/u;->f(B)I

    move-result v0

    if-nez v0, :cond_6

    const-string v0, "\u6e9c\u5ba0"

    invoke-virtual {v2, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :goto_2
    invoke-virtual {v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;)V

    goto/16 :goto_0

    :cond_5
    const/4 v4, 0x1

    if-ne v3, v4, :cond_4

    const-string v3, "\u5f85\u547d"

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :cond_6
    const-string v0, "\u9690\u85cf"

    invoke-virtual {v2, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_2

    :cond_7
    iget-object v1, p0, Lpmsj/work/e/cn;->r:Lpmsj/work/d/c;

    if-eqz v1, :cond_0

    iget-object v1, p0, Lpmsj/work/e/cn;->r:Lpmsj/work/d/c;

    invoke-virtual {v1, v0}, Lpmsj/work/d/c;->b(Lpmsj/work/b/n;)Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/cn;->ae()V

    :try_start_0
    iget-object p0, p0, Lpmsj/work/e/cn;->r:Lpmsj/work/d/c;

    check-cast p0, Lpmsj/work/e/w;

    invoke-virtual {p0}, Lpmsj/work/e/w;->i()Ljava/lang/String;

    move-result-object v0

    const-string v1, "\u804a\u5929"

    const/16 v2, 0x50

    const/4 v3, 0x0

    invoke-static {v1, v2, v3, v0, p0}, Lpmsj/work/c/a;->a(Ljava/lang/String;IILjava/lang/String;Lpmsj/work/a/a;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto/16 :goto_0

    :catch_0
    move-exception v0

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0xb79b
        :pswitch_0
    .end packed-switch
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 10

    const/4 v7, 0x2

    const/16 v5, 0x9

    const/16 v6, 0x46a

    const/4 v3, 0x0

    const/4 v9, 0x1

    iget-object v1, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v1}, Lpmsj/work/d/g;->g()I

    move-result v1

    iget-object v2, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    if-lt v1, v2, :cond_0

    move v1, v9

    :goto_0
    return v1

    :cond_0
    iget-object v1, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iget-object v2, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v2}, Lpmsj/work/d/g;->g()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    move-object v0, v1

    check-cast v0, Lpmsj/work/b/n;

    move-object v4, v0

    const-string v1, "\u5c5e\u6027"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_2

    iput-object v4, p0, Lpmsj/work/e/cn;->O:Lpmsj/work/b/n;

    check-cast v4, Lpmsj/work/b/u;

    invoke-static {v4}, Lpmsj/work/main/j;->a(Lpmsj/work/b/u;)V

    :cond_1
    :goto_1
    move v1, v9

    goto :goto_0

    :cond_2
    const-string v1, "\u5f85\u547d"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_3

    const/16 v1, 0xa

    invoke-virtual {v4}, Lpmsj/work/b/n;->u()I

    move-result v2

    invoke-static {v6, v1, v2, v3}, Lpmsj/work/main/w;->a(IBIB)V

    goto :goto_1

    :cond_3
    const-string v1, "\u51fa\u6218"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_6

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->c()I

    move-result v1

    invoke-virtual {v4, v5}, Lpmsj/work/b/n;->f(B)I

    move-result v2

    if-le v2, v1, :cond_4

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "\u51fa\u6218\u8be5\u5ba0\u7269\u9700\u8981\u7b49\u7ea7\u8fbe\u5230"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v4, v5}, Lpmsj/work/b/n;->f(B)I

    move-result v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_1

    :cond_4
    invoke-virtual {v4}, Lpmsj/work/b/n;->c()I

    move-result v2

    sub-int v1, v2, v1

    const/4 v2, 0x5

    if-le v1, v2, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const-string v2, "\u8be5\u5ba0\u7269\u7b49\u7ea7\u9ad8\u4e8e\u60a85\u7ea7\u4ee5\u4e0a,\u4e0d\u53ef\u51fa\u6218."

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_1

    :cond_5
    const/16 v1, 0xa

    invoke-virtual {v4}, Lpmsj/work/b/n;->u()I

    move-result v2

    invoke-static {v6, v1, v2, v9}, Lpmsj/work/main/w;->a(IBIB)V

    goto :goto_1

    :cond_6
    const-string v1, "\u6539\u540d"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_7

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const-string v2, "\u8bf7\u8f93\u5165\u4e00\u4e2a\u65b0\u7684\u540d\u5b57\uff1a"

    const/4 v5, 0x7

    const-string v6, "\u5ba0\u7269\u6539\u540d"

    invoke-virtual {v4}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v8

    move-object v4, p0

    move v7, v3

    invoke-virtual/range {v1 .. v8}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    goto :goto_1

    :cond_7
    const-string v1, "\u653e\u751f"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_8

    const/4 v1, 0x0

    const-string v2, "\u60a8\u786e\u5b9a\u8981\u653e\u5f03"

    invoke-static {v1, v2}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v1

    invoke-virtual {v4}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "\uff1f"

    invoke-static {v1, v2}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v2

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v2, v1, v3, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto/16 :goto_1

    :cond_8
    const-string v1, "\u6e9c\u5ba0"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_9

    const/16 v1, 0x30

    invoke-virtual {v4}, Lpmsj/work/b/n;->u()I

    move-result v2

    invoke-static {v6, v1, v2, v9}, Lpmsj/work/main/w;->a(IBIB)V

    goto/16 :goto_1

    :cond_9
    const-string v1, "\u9690\u85cf"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_a

    const/16 v1, 0x30

    invoke-virtual {v4}, Lpmsj/work/b/n;->u()I

    move-result v2

    invoke-static {v6, v1, v2, v3}, Lpmsj/work/main/w;->a(IBIB)V

    goto/16 :goto_1

    :cond_a
    const-string v1, "\u653e\u5165"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_b

    iget-object v1, p0, Lpmsj/work/e/cn;->r:Lpmsj/work/d/c;

    if-eqz v1, :cond_1

    iget-object v1, p0, Lpmsj/work/e/cn;->r:Lpmsj/work/d/c;

    invoke-virtual {v1, v4}, Lpmsj/work/d/c;->b(Lpmsj/work/b/n;)Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual {p0, v3}, Lpmsj/work/e/cn;->a(Z)V

    goto/16 :goto_1

    :cond_b
    const-string v1, "\u67e5\u770b"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_d

    iput-object v4, p0, Lpmsj/work/e/cn;->O:Lpmsj/work/b/n;

    invoke-virtual {v4}, Lpmsj/work/b/n;->u()I

    move-result v1

    sget-object v2, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v2}, Lpmsj/work/b/ab;->u()I

    move-result v2

    if-ne v1, v2, :cond_c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    goto/16 :goto_1

    :cond_c
    check-cast v4, Lpmsj/work/b/u;

    invoke-static {v4}, Lpmsj/work/main/j;->a(Lpmsj/work/b/u;)V

    goto/16 :goto_1

    :cond_d
    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_e

    const-string v1, "\u6446\u644a"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_10

    :cond_e
    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_f

    move v3, v9

    :goto_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "\u8bf7\u8f93\u5165\u552e\u4ef7 "

    invoke-virtual {v2, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v4}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    const-string v6, "\u8bf7\u8f93\u5165\u552e\u4ef7"

    const-string v8, ""

    move-object v4, p0

    invoke-virtual/range {v1 .. v8}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    goto/16 :goto_1

    :cond_f
    move v3, v7

    goto :goto_2

    :cond_10
    const-string v1, "\u5bc4\u5b58"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual {p0}, Lpmsj/work/e/cn;->af()I

    move-result v1

    if-ne v1, v9, :cond_11

    const/4 v1, 0x6

    invoke-virtual {v4, v9}, Lpmsj/work/b/n;->f(B)I

    move-result v2

    invoke-static {v6, v1, v2}, Lpmsj/work/main/w;->a(IBI)V

    :goto_3
    invoke-static {v9, v3}, Lpmsj/work/main/t;->a(ZZ)V

    goto/16 :goto_1

    :cond_11
    const/4 v1, 0x3

    invoke-virtual {v4, v9}, Lpmsj/work/b/n;->f(B)I

    move-result v2

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/m;->h()I

    move-result v4

    invoke-static {v6, v1, v2, v4}, Lpmsj/work/main/w;->a(IBII)V

    goto :goto_3
.end method

.method protected final c()V
    .locals 2

    const v0, 0xb79b

    invoke-virtual {p0, v0}, Lpmsj/work/e/cn;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/g;

    iput-object v0, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    iget-object v0, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    const/16 v1, 0x80

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->l(I)V

    const v0, 0xb799

    invoke-virtual {p0, v0}, Lpmsj/work/e/cn;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/cn;->P:Lpmsj/work/d/l;

    iget-object v0, p0, Lpmsj/work/e/cn;->P:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->p()V

    iget-object v0, p0, Lpmsj/work/e/cn;->P:Lpmsj/work/d/l;

    const/4 v1, 0x2

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->l(I)V

    return-void
.end method

.method public final c(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 19

    invoke-super/range {p0 .. p3}, Lpmsj/work/d/c;->c(Ljavax/microedition/lcdui/Graphics;II)V

    move-object/from16 v0, p0

    iget-boolean v0, v0, Lpmsj/work/e/cn;->K:Z

    move v4, v0

    if-eqz v4, :cond_2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    if-eqz v4, :cond_2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/util/Vector;->size()I

    move-result v4

    if-lez v4, :cond_2

    const/4 v4, 0x0

    move v11, v4

    :goto_0
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/util/Vector;->size()I

    move-result v4

    if-ge v11, v4, :cond_2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4, v11}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Lpmsj/work/b/n;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    mul-int/lit8 v6, v11, 0x2

    add-int/lit8 v6, v6, 0x1

    invoke-virtual {v5, v6}, Lpmsj/work/d/g;->a(I)Lpmsj/work/d/b;

    move-result-object v5

    check-cast v5, Lpmsj/work/d/l;

    if-eqz v5, :cond_2

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/4 v7, 0x0

    const/4 v8, 0x0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v9

    if-ne v4, v9, :cond_0

    const/16 v5, 0x28

    invoke-virtual {v4, v5}, Lpmsj/work/b/n;->f(B)I

    move-result v5

    const/16 v6, 0x29

    invoke-virtual {v4, v6}, Lpmsj/work/b/n;->f(B)I

    move-result v6

    const/16 v7, 0x2a

    invoke-virtual {v4, v7}, Lpmsj/work/b/n;->f(B)I

    move-result v7

    const/16 v8, 0x2b

    invoke-virtual {v4, v8}, Lpmsj/work/b/n;->f(B)I

    move-result v4

    move v12, v4

    move v13, v7

    move v14, v6

    move v15, v5

    :goto_1
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v4, v0

    iget-short v4, v4, Lpmsj/work/d/b;->i:S

    add-int/lit8 v7, v4, 0x41

    if-lez v7, :cond_2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v4, v0

    iget-short v4, v4, Lpmsj/work/d/b;->j:S

    add-int/lit8 v5, v11, 0x1

    mul-int/lit8 v5, v5, 0x54

    add-int/2addr v4, v5

    const/16 v5, 0x16

    sub-int v8, v4, v5

    add-int/lit16 v4, v7, 0xa0

    add-int/lit8 v16, v4, 0x5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->V:Lpmsj/work/a/i;

    move-object v4, v0

    invoke-virtual {v4}, Lpmsj/work/a/i;->b()I

    move-result v4

    const/16 v5, 0xa

    sub-int/2addr v4, v5

    div-int/lit8 v4, v4, 0x2

    add-int v17, v8, v4

    const/16 v4, 0xa0

    invoke-static {v4, v14, v15}, La/c/x;->a(III)I

    move-result v18

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->aa:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->X:Lpmsj/work/a/i;

    move-object v6, v0

    const/16 v9, 0xa0

    move-object/from16 v4, p1

    invoke-static/range {v4 .. v9}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;III)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->Y:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->V:Lpmsj/work/a/i;

    move-object v6, v0

    const/16 v10, 0xa0

    move-object/from16 v4, p1

    move/from16 v9, v18

    invoke-static/range {v4 .. v10}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;IIII)V

    new-instance v4, Lpmsj/work/d/d;

    const/16 v5, 0x1a

    const/16 v6, 0x8

    const v9, 0x54d8bb

    invoke-direct {v4, v5, v6, v9}, Lpmsj/work/d/d;-><init>(III)V

    move-object v0, v4

    move/from16 v1, v16

    move/from16 v2, v17

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/d;->f(II)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v5, v0

    const/4 v6, 0x0

    invoke-virtual {v5, v6}, Ljava/lang/StringBuffer;->setLength(I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v5, v0

    invoke-virtual {v5, v15}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v5, v0

    const/16 v6, 0x2f

    invoke-virtual {v5, v6}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v5, v0

    invoke-virtual {v5, v14}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Lpmsj/work/d/d;->b(Ljava/lang/String;)V

    move-object v0, v4

    move-object/from16 v1, p1

    move/from16 v2, p2

    move/from16 v3, p3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    add-int/lit8 v8, v8, 0xa

    const/16 v4, 0xa0

    invoke-static {v4, v12, v13}, La/c/x;->a(III)I

    move-result v14

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->aa:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->X:Lpmsj/work/a/i;

    move-object v6, v0

    const/16 v9, 0xa0

    move-object/from16 v4, p1

    invoke-static/range {v4 .. v9}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;III)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->Z:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->W:Lpmsj/work/a/i;

    move-object v6, v0

    const/16 v10, 0xa0

    move-object/from16 v4, p1

    move v9, v14

    invoke-static/range {v4 .. v10}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;IIII)V

    add-int/lit8 v4, v17, 0xa

    new-instance v5, Lpmsj/work/d/d;

    const/16 v6, 0x1a

    const/16 v7, 0x8

    const v8, 0x54d8bb

    invoke-direct {v5, v6, v7, v8}, Lpmsj/work/d/d;-><init>(III)V

    move-object v0, v5

    move/from16 v1, v16

    move v2, v4

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/d;->f(II)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v4, v0

    const/4 v6, 0x0

    invoke-virtual {v4, v6}, Ljava/lang/StringBuffer;->setLength(I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v4, v0

    invoke-virtual {v4, v13}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v4, v0

    const/16 v6, 0x2f

    invoke-virtual {v4, v6}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v4, v0

    invoke-virtual {v4, v12}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->ad:Ljava/lang/StringBuffer;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v5, v4}, Lpmsj/work/d/d;->b(Ljava/lang/String;)V

    move-object v0, v5

    move-object/from16 v1, p1

    move/from16 v2, p2

    move/from16 v3, p3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    add-int/lit8 v4, v11, 0x1

    move v11, v4

    goto/16 :goto_0

    :cond_0
    instance-of v9, v4, Lpmsj/work/b/u;

    if-eqz v9, :cond_1

    const/16 v5, 0x26

    invoke-virtual {v4, v5}, Lpmsj/work/b/n;->f(B)I

    move-result v5

    const/16 v6, 0x27

    invoke-virtual {v4, v6}, Lpmsj/work/b/n;->f(B)I

    move-result v6

    const/16 v7, 0x28

    invoke-virtual {v4, v7}, Lpmsj/work/b/n;->f(B)I

    move-result v7

    const/16 v8, 0x29

    invoke-virtual {v4, v8}, Lpmsj/work/b/n;->f(B)I

    move-result v4

    move v12, v4

    move v13, v7

    move v14, v6

    move v15, v5

    goto/16 :goto_1

    :cond_1
    iget v4, v4, Lpmsj/work/b/n;->j:I

    invoke-static {v4}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v4

    if-eqz v4, :cond_a

    const/4 v5, 0x3

    aget-object v5, v4, v5

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    const/4 v6, 0x2

    aget-object v6, v4, v6

    invoke-virtual {v6}, La/c/i;->b()I

    move-result v6

    const/4 v7, 0x6

    aget-object v7, v4, v7

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v7

    const/4 v8, 0x7

    aget-object v4, v4, v8

    invoke-virtual {v4}, La/c/i;->b()I

    move-result v4

    move v12, v4

    move v13, v7

    move v14, v6

    move v15, v5

    goto/16 :goto_1

    :cond_2
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    if-eqz v4, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/util/Vector;->size()I

    move-result v4

    if-lez v4, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    move-object v4, v0

    if-nez v4, :cond_3

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    if-eqz v4, :cond_3

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/util/Vector;->size()I

    move-result v4

    new-array v4, v4, [Lpmsj/work/a/b;

    move-object v0, v4

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    :cond_3
    const/4 v4, 0x0

    :goto_2
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v5

    if-ge v4, v5, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lpmsj/work/b/n;

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v5, v0

    mul-int/lit8 v6, v4, 0x2

    invoke-virtual {v5, v6}, Lpmsj/work/d/g;->a(I)Lpmsj/work/d/b;

    move-result-object p3

    check-cast p3, Lpmsj/work/d/a;

    const/4 v5, 0x0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v6

    move-object/from16 v0, p2

    move-object v1, v6

    if-ne v0, v1, :cond_7

    const/16 v5, 0x26

    move-object/from16 v0, p2

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/n;->f(B)I

    move-result v5

    :cond_4
    :goto_3
    if-lez v5, :cond_6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    move-object v5, v0

    aget-object v5, v5, v4

    if-nez v5, :cond_5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    move-object v5, v0

    new-instance v6, Lpmsj/work/a/b;

    const v7, 0x596cfe

    invoke-direct {v6, v7}, Lpmsj/work/a/b;-><init>(I)V

    aput-object v6, v5, v4

    :cond_5
    move-object/from16 v0, p3

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    if-lez v5, :cond_6

    move-object/from16 v0, p0

    iget-boolean v0, v0, Lpmsj/work/e/cn;->d:Z

    move v5, v0

    if-eqz v5, :cond_8

    const/16 v5, -0xa

    :goto_4
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    move-object v6, v0

    aget-object v6, v6, v4

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    move-object v7, v0

    iget-short v7, v7, Lpmsj/work/d/b;->i:S

    add-int/lit8 v7, v7, 0x2

    invoke-virtual/range {p3 .. p3}, Lpmsj/work/d/a;->E()I

    move-result v8

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/e/cn;->U:[Lpmsj/work/a/b;

    move-object v9, v0

    aget-object v9, v9, v4

    invoke-virtual {v9}, Lpmsj/work/a/b;->b()I

    move-result v9

    sub-int/2addr v8, v9

    add-int/2addr v5, v8

    move-object v0, v6

    move-object/from16 v1, p1

    move v2, v7

    move v3, v5

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/a/b;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_6
    add-int/lit8 v4, v4, 0x1

    goto/16 :goto_2

    :cond_7
    move-object/from16 v0, p2

    instance-of v0, v0, Lpmsj/work/b/u;

    move v6, v0

    if-eqz v6, :cond_4

    const/16 v5, 0x25

    move-object/from16 v0, p2

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/n;->f(B)I

    move-result v5

    goto :goto_3

    :cond_8
    const/4 v5, -0x5

    goto :goto_4

    :cond_9
    return-void

    :cond_a
    move v12, v8

    move v13, v7

    move v14, v6

    move v15, v5

    goto/16 :goto_1
.end method

.method public final c_(I)V
    .locals 3

    if-nez p1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/cn;->e:Ljava/util/Vector;

    iget-object v1, p0, Lpmsj/work/e/cn;->c:Lpmsj/work/d/g;

    invoke-virtual {v1}, Lpmsj/work/d/g;->g()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Lpmsj/work/b/u;

    const/16 v0, 0x46a

    const/4 v1, 0x1

    invoke-virtual {p0}, Lpmsj/work/b/u;->u()I

    move-result v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(IBI)V

    :cond_0
    return-void
.end method

.method public final i()Z
    .locals 4

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/e/cn;->O:Lpmsj/work/b/n;

    if-nez v0, :cond_0

    move v0, v3

    :goto_0
    return v0

    :cond_0
    move v1, v3

    :goto_1
    sget-object v0, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v1, v0, :cond_2

    sget-object v0, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    iget-object v2, p0, Lpmsj/work/e/cn;->O:Lpmsj/work/b/n;

    invoke-virtual {v2}, Lpmsj/work/b/n;->u()I

    move-result v2

    invoke-virtual {v0}, Lpmsj/work/b/n;->u()I

    move-result v0

    if-ne v2, v0, :cond_1

    const/4 v0, 0x1

    goto :goto_0

    :cond_1
    add-int/lit8 v0, v1, 0x1

    move v1, v0

    goto :goto_1

    :cond_2
    move v0, v3

    goto :goto_0
.end method

.method public final y(I)V
    .locals 0

    invoke-super {p0, p1}, Lpmsj/work/d/c;->y(I)V

    return-void
.end method
