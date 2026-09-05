.class public final Lpmsj/work/b/h;
.super Lpmsj/work/b/v;


# static fields
.field private static final L:La/b/c;

.field private static final M:La/b/c;

.field private static aa:Lpmsj/work/a/i;

.field public static h:La/c/q;

.field public static i:Z


# instance fields
.field private K:Z

.field private N:La/b/c;

.field private O:La/b/c;

.field private P:La/c/q;

.field private Q:B

.field private R:Z

.field private S:I

.field private T:I

.field private U:B

.field private V:Ljava/util/Vector;

.field private W:Ljava/util/Vector;

.field private X:Ljava/util/Vector;

.field private Y:Ljava/util/Vector;

.field private Z:Ljava/util/Vector;

.field private ab:I


# direct methods
.method static constructor <clinit>()V
    .locals 3

    const/16 v2, 0x12

    new-instance v0, La/b/c;

    const/16 v1, 0xf

    invoke-direct {v0, v2, v1}, La/b/c;-><init>(II)V

    sput-object v0, Lpmsj/work/b/h;->L:La/b/c;

    new-instance v0, La/b/c;

    const/4 v1, 0x5

    invoke-direct {v0, v2, v1}, La/b/c;-><init>(II)V

    sput-object v0, Lpmsj/work/b/h;->M:La/b/c;

    new-instance v0, La/c/q;

    const/16 v1, 0x3e8

    invoke-direct {v0, v1}, La/c/q;-><init>(I)V

    sput-object v0, Lpmsj/work/b/h;->h:La/c/q;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x8aded2

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/h;->aa:Lpmsj/work/a/i;

    return-void
.end method

.method public constructor <init>(IBII)V
    .locals 6

    const/4 v5, 0x0

    move-object v0, p0

    move v1, p1

    move v2, p2

    move v3, p3

    move v4, p4

    invoke-direct/range {v0 .. v5}, Lpmsj/work/b/v;-><init>(IBIIZ)V

    new-instance v0, La/b/c;

    invoke-direct {v0, v5, v5}, La/b/c;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/b/h;->N:La/b/c;

    new-instance v0, La/b/c;

    invoke-direct {v0, v5, v5}, La/b/c;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/b/h;->O:La/b/c;

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/h;->P:La/c/q;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/h;->W:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/h;->X:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/h;->Y:Ljava/util/Vector;

    return-void
.end method

.method public static b(II)V
    .locals 10

    const/4 v9, 0x0

    const/16 v0, 0x411

    new-instance v1, La/c/m;

    const/16 v2, 0xa

    invoke-direct {v1, v2}, La/c/m;-><init>(I)V

    new-instance v2, La/c/h;

    int-to-byte v3, p0

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    invoke-direct {v3, p1}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    invoke-direct {v4, v9}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    invoke-direct {v5, v9}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    invoke-direct {v6, v9}, La/c/m;-><init>(I)V

    new-instance v7, La/c/m;

    invoke-direct {v7, v9}, La/c/m;-><init>(I)V

    new-instance v8, La/c/m;

    invoke-direct {v8, v9}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v8}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    return-void
.end method

.method public static f(I)I
    .locals 3

    const v0, 0x186a0

    invoke-static {p0}, Lpmsj/work/b/h;->K(I)I

    move-result v1

    const/4 v2, 0x1

    packed-switch v1, :pswitch_data_0

    move v1, v2

    :goto_0
    mul-int/lit16 v1, v1, 0x2710

    add-int/2addr v0, v1

    return v0

    :pswitch_0
    const/4 v1, 0x2

    goto :goto_0

    :pswitch_1
    const/4 v1, 0x3

    goto :goto_0

    :pswitch_2
    const/4 v1, 0x4

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0xb
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method


# virtual methods
.method public final a()I
    .locals 1

    const/4 v0, 0x7

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    return v0
.end method

.method public final a(B)V
    .locals 0

    iput-byte p1, p0, Lpmsj/work/b/h;->Q:B

    return-void
.end method

.method public final a(BSSILjava/lang/String;)V
    .locals 6

    new-instance v0, La/c/a;

    const/4 v1, 0x6

    invoke-direct {v0, v1}, La/c/a;-><init>(I)V

    iget-object v1, v0, La/c/a;->a:[La/c/i;

    const/4 v2, 0x0

    new-instance v3, La/c/h;

    invoke-direct {v3, p1}, La/c/h;-><init>(B)V

    aput-object v3, v1, v2

    const/4 v2, 0x1

    new-instance v3, La/c/o;

    invoke-direct {v3, p2}, La/c/o;-><init>(S)V

    aput-object v3, v1, v2

    const/4 v2, 0x2

    new-instance v3, La/c/o;

    invoke-direct {v3, p3}, La/c/o;-><init>(S)V

    aput-object v3, v1, v2

    iget-object v2, p0, Lpmsj/work/b/h;->N:La/b/c;

    iget-short v2, v2, La/b/c;->a:S

    sub-int v2, p2, v2

    invoke-static {v2}, Ljava/lang/Math;->abs(I)I

    move-result v2

    iget-object v3, p0, Lpmsj/work/b/h;->N:La/b/c;

    iget-short v3, v3, La/b/c;->b:S

    sub-int v3, p3, v3

    invoke-static {v3}, Ljava/lang/Math;->abs(I)I

    move-result v3

    invoke-static {v2, v3}, Ljava/lang/Math;->max(II)I

    move-result v2

    mul-int/lit8 v2, v2, 0x2

    const/4 v3, 0x3

    new-instance v4, La/c/o;

    int-to-short v2, v2

    invoke-direct {v4, v2}, La/c/o;-><init>(S)V

    aput-object v4, v1, v3

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    int-to-long v4, p4

    add-long/2addr v2, v4

    const/4 v4, 0x4

    new-instance v5, La/c/n;

    invoke-direct {v5, v2, v3}, La/c/n;-><init>(J)V

    aput-object v5, v1, v4

    if-eqz p5, :cond_0

    const/4 v2, 0x5

    new-instance v3, La/c/p;

    invoke-direct {v3, p5}, La/c/p;-><init>(Ljava/lang/String;)V

    aput-object v3, v1, v2

    :cond_0
    iget-object v1, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    return-void
.end method

.method public final a(II)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/h;->N:La/b/c;

    invoke-virtual {v0, p1, p2}, La/b/c;->a(II)V

    return-void
.end method

.method public final a(IIII)V
    .locals 1

    int-to-byte v0, p1

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->b(B)V

    iget-object v0, p0, Lpmsj/work/b/h;->O:La/b/c;

    invoke-virtual {v0, p2, p3}, La/b/c;->a(II)V

    iget-object v0, p0, Lpmsj/work/b/h;->P:La/c/q;

    invoke-virtual {v0, p4}, La/c/q;->e(I)V

    return-void
.end method

.method public final a(IIIIII)V
    .locals 9

    const/4 v0, 0x7

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v5

    const/16 v0, 0x411

    new-instance v1, La/c/m;

    invoke-direct {v1, p1}, La/c/m;-><init>(I)V

    new-instance v2, La/c/h;

    int-to-byte v3, p2

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v4

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    invoke-direct {v5, p3}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    invoke-direct {v6, p4}, La/c/m;-><init>(I)V

    new-instance v7, La/c/m;

    invoke-direct {v7, p5}, La/c/m;-><init>(I)V

    new-instance v8, La/c/m;

    invoke-direct {v8, p6}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v8}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    return-void
.end method

.method public final a(IZ)V
    .locals 5

    const/4 v4, 0x3

    if-lez p1, :cond_2

    const v0, 0x5504ea

    :goto_0
    new-instance v1, Lpmsj/work/d/d;

    const/16 v2, 0x64

    const/16 v3, 0xa

    invoke-direct {v1, v2, v3, v0}, Lpmsj/work/d/d;-><init>(III)V

    const/high16 v0, 0x800000

    sget-byte v2, Lpmsj/work/d/d;->a:B

    or-int/2addr v0, v2

    invoke-virtual {v1, v0}, Lpmsj/work/d/d;->l(I)V

    invoke-virtual {v1, p1}, Lpmsj/work/d/d;->a(I)V

    invoke-virtual {v1}, Lpmsj/work/d/d;->c()V

    iget-object v0, p0, Lpmsj/work/b/h;->W:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-virtual {p0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    add-int/2addr v0, p1

    const/4 v1, 0x0

    invoke-static {v1, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    const/16 v1, 0xb

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    iget v2, p0, Lpmsj/work/b/h;->S:I

    add-int/2addr v1, v2

    invoke-static {v0, v1}, Ljava/lang/Math;->min(II)I

    move-result v0

    invoke-virtual {p0, v4, v0}, Lpmsj/work/b/h;->a(BI)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->u()I

    move-result v2

    if-ne v1, v2, :cond_4

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    const/16 v2, 0x28

    invoke-virtual {v1, v2, v0}, Lpmsj/work/b/ab;->a(BI)V

    :cond_0
    :goto_1
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    iget-byte v1, v1, Lpmsj/work/main/b;->d:B

    if-eq v1, v4, :cond_1

    const/4 v1, 0x5

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    iget-byte v2, v2, Lpmsj/work/main/b;->d:B

    if-ne v1, v2, :cond_1

    const/4 v1, 0x1

    const/4 v2, 0x7

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    if-ne v1, v2, :cond_1

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    invoke-static {v1}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v1

    if-eqz v1, :cond_1

    aget-object v1, v1, v4

    invoke-virtual {v1, v0}, La/c/i;->a(I)V

    :cond_1
    return-void

    :cond_2
    if-eqz p2, :cond_3

    const v0, 0x5a1187

    goto :goto_0

    :cond_3
    const v0, 0x5a350a

    goto/16 :goto_0

    :cond_4
    sget-object v1, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-eqz v1, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    invoke-virtual {v2}, Lpmsj/work/b/u;->u()I

    move-result v2

    if-ne v1, v2, :cond_0

    sget-object v1, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v2, 0x26

    invoke-virtual {v1, v2, v0}, Lpmsj/work/b/u;->a(BI)V

    goto :goto_1
.end method

.method public final a(Ljava/lang/String;)V
    .locals 6

    const/4 v1, 0x1

    iget-short v2, p0, Lpmsj/work/b/h;->w:S

    iget-short v3, p0, Lpmsj/work/b/h;->x:S

    const/4 v4, 0x0

    move-object v0, p0

    move-object v5, p1

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/b/h;->a(BSSILjava/lang/String;)V

    return-void
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 3

    const/4 v2, 0x5

    sget-boolean v0, Lpmsj/work/main/f;->a:Z

    if-nez v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    if-eq v0, v1, :cond_0

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->a(I)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x3

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_1

    :cond_0
    const/16 v0, 0x8

    sub-int v0, p3, v0

    sub-int/2addr v0, v2

    invoke-super {p0, p1, p2, v0}, Lpmsj/work/b/v;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_1
    return-void
.end method

.method public final a(Z)V
    .locals 0

    iput-boolean p1, p0, Lpmsj/work/b/h;->K:Z

    return-void
.end method

.method public final a(I)Z
    .locals 2

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    and-int/2addr v0, p1

    if-ne v0, p1, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final b(B)V
    .locals 2

    const/16 v1, 0x63

    if-ne v1, p1, :cond_2

    iget-byte v0, p0, Lpmsj/work/b/h;->U:B

    if-eq v1, v0, :cond_0

    const v0, 0x1f20c0

    const/4 v1, 0x0

    invoke-static {v0, v1}, La/a/d;->a(IZ)La/a/d;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    :cond_0
    :goto_0
    iput-byte p1, p0, Lpmsj/work/b/h;->U:B

    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    iget-byte v1, p0, Lpmsj/work/b/h;->n:B

    invoke-virtual {v0, p1, v1}, La/a/d;->b(II)I

    move-result v0

    const/4 v1, -0x1

    if-eq v1, v0, :cond_1

    iget-object v1, p0, Lpmsj/work/b/h;->o:La/a/d;

    invoke-virtual {v1, v0}, La/a/d;->d(I)V

    :cond_1
    return-void

    :cond_2
    iget-byte v0, p0, Lpmsj/work/b/h;->U:B

    if-ne v1, v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/h;->A()V

    invoke-virtual {p0}, Lpmsj/work/b/h;->r()V

    goto :goto_0
.end method

.method public final b(I)V
    .locals 1

    iget v0, p0, Lpmsj/work/b/h;->S:I

    add-int/2addr v0, p1

    iput v0, p0, Lpmsj/work/b/h;->S:I

    return-void
.end method

.method public final b(Ljava/lang/String;)V
    .locals 6

    const/4 v3, 0x0

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    new-instance v0, Lpmsj/work/b/s;

    invoke-direct {v0}, Lpmsj/work/b/s;-><init>()V

    const/16 v2, 0x50

    move-object v1, p1

    move v4, v3

    move v5, v3

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/b/s;->b(Ljava/lang/String;IIII)La/b/c;

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v1

    if-nez v1, :cond_1

    const/16 v1, 0x14

    :goto_1
    invoke-virtual {p0}, Lpmsj/work/b/h;->t()I

    move-result v2

    div-int/lit8 v2, v2, 0x2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/s;->d(II)V

    iget-object v1, p0, Lpmsj/work/b/h;->Y:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_0

    :cond_1
    const/16 v1, -0x14

    goto :goto_1
.end method

.method public final b()Z
    .locals 1

    iget-boolean v0, p0, Lpmsj/work/b/h;->K:Z

    return v0
.end method

.method public final b(Ljavax/microedition/lcdui/Graphics;II)Z
    .locals 21

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->P:La/c/q;

    move-object v5, v0

    invoke-virtual {v5}, La/c/q;->h()Z

    move-result v5

    if-eqz v5, :cond_3

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->P:La/c/q;

    move-object v5, v0

    invoke-virtual {v5}, La/c/q;->j()I

    move-result v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->P:La/c/q;

    move-object v6, v0

    invoke-virtual {v6}, La/c/q;->k()I

    move-result v6

    invoke-static {v6, v5}, Ljava/lang/Math;->min(II)I

    move-result v6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->O:La/b/c;

    move-object v7, v0

    iget-short v7, v7, La/b/c;->a:S

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v8, v0

    iget-short v8, v8, La/b/c;->a:S

    sub-int/2addr v7, v8

    invoke-static {v7, v5, v6}, La/c/x;->a(III)I

    move-result v7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->O:La/b/c;

    move-object v8, v0

    iget-short v8, v8, La/b/c;->b:S

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v9, v0

    iget-short v9, v9, La/b/c;->b:S

    sub-int/2addr v8, v9

    invoke-static {v8, v5, v6}, La/c/x;->a(III)I

    move-result v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v6, v0

    iget-short v6, v6, La/b/c;->a:S

    add-int/2addr v6, v7

    add-int v6, v6, p2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v7, v0

    iget-short v7, v7, La/b/c;->b:S

    add-int/2addr v5, v7

    add-int v5, v5, p3

    move-object/from16 v0, p0

    iget-boolean v0, v0, Lpmsj/work/b/h;->R:Z

    move v7, v0

    if-eqz v7, :cond_2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->P:La/c/q;

    move-object v7, v0

    invoke-virtual {v7}, La/c/q;->i()Z

    move-result v7

    if-eqz v7, :cond_2

    const/4 v7, 0x1

    :goto_0
    move v13, v7

    move v14, v5

    move v15, v6

    :goto_1
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->o:La/a/d;

    move-object v5, v0

    if-eqz v5, :cond_0

    const/4 v5, 0x2

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->n(I)Z

    move-result v5

    if-eqz v5, :cond_5

    const/4 v5, 0x1

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/b/h;->U:B

    move v6, v0

    if-ne v5, v6, :cond_5

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    long-to-int v5, v5

    div-int/lit16 v5, v5, 0x2bc

    rem-int/lit8 v5, v5, 0x2

    if-nez v5, :cond_0

    const/16 v5, 0x8

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->n(I)Z

    move-result v5

    if-eqz v5, :cond_4

    const/4 v5, 0x1

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/b/h;->U:B

    move v6, v0

    if-ne v5, v6, :cond_4

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->o:La/a/d;

    move-object v5, v0

    move-object v0, v5

    move v1, v15

    move v2, v14

    move-object/from16 v3, p1

    invoke-virtual {v0, v1, v2, v3}, La/a/d;->a(IILjavax/microedition/lcdui/Graphics;)V

    :cond_0
    :goto_2
    const/16 v5, 0x63

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/b/h;->U:B

    move v6, v0

    if-eq v5, v6, :cond_1

    const/16 v5, 0xa

    sub-int v6, v15, v5

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/b/h;->t()I

    move-result v5

    sub-int v16, v14, v5

    const/16 v5, 0xc

    sub-int v7, v16, v5

    const/4 v8, 0x6

    const/16 v5, 0xb

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v9

    const/4 v5, 0x3

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v10

    sget v11, Lpmsj/work/a/c;->A:I

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/b/h;->S:I

    move v12, v0

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v12}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIII)V

    const/16 v5, 0xc

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v9

    if-lez v9, :cond_1

    const/4 v5, 0x6

    sub-int v7, v16, v5

    const/4 v8, 0x4

    const/16 v5, 0xa

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v10

    sget v11, Lpmsj/work/a/c;->D:I

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/b/h;->T:I

    move v12, v0

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v12}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIII)V

    :cond_1
    sget-boolean v5, Lpmsj/work/b/h;->i:Z

    if-eqz v5, :cond_8

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/b/h;->t()I

    move-result v5

    sub-int v5, v14, v5

    sget-object v6, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v6}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v6

    sub-int/2addr v5, v6

    const/16 v6, 0x8

    sub-int v11, v5, v6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    move-object v5, v0

    if-eqz v5, :cond_8

    sget-object v5, Lpmsj/work/b/h;->aa:Lpmsj/work/a/i;

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v12

    sget-object v5, Lpmsj/work/b/h;->aa:Lpmsj/work/a/i;

    invoke-virtual {v5}, Lpmsj/work/a/i;->b()I

    move-result v16

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v17

    const/4 v5, 0x0

    const/4 v6, 0x0

    move/from16 v18, v6

    move/from16 v19, v5

    :goto_3
    move/from16 v0, v18

    move/from16 v1, v17

    if-ge v0, v1, :cond_8

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    move-object v5, v0

    move-object v0, v5

    move/from16 v1, v18

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Ljava/lang/Integer;

    rem-int/lit8 v5, v18, 0x2

    if-nez v5, :cond_7

    add-int v19, v19, v16

    sget-object v5, Lpmsj/work/b/h;->aa:Lpmsj/work/a/i;

    sub-int v7, v15, v12

    sub-int v8, v11, v19

    invoke-virtual/range {p2 .. p2}, Ljava/lang/Integer;->intValue()I

    move-result v9

    const/4 v10, 0x0

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move/from16 v5, v19

    :goto_4
    add-int/lit8 v6, v18, 0x1

    move/from16 v18, v6

    move/from16 v19, v5

    goto :goto_3

    :cond_2
    const/4 v7, 0x0

    goto/16 :goto_0

    :cond_3
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v5, v0

    iget-short v5, v5, La/b/c;->a:S

    add-int v5, v5, p2

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->N:La/b/c;

    move-object v6, v0

    iget-short v6, v6, La/b/c;->b:S

    add-int v6, v6, p3

    const/4 v7, 0x0

    move v13, v7

    move v14, v6

    move v15, v5

    goto/16 :goto_1

    :cond_4
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->o:La/a/d;

    move-object v5, v0

    move-object v0, v5

    move v1, v15

    move v2, v14

    move-object/from16 v3, p1

    invoke-virtual {v0, v1, v2, v3}, La/a/d;->b(IILjavax/microedition/lcdui/Graphics;)V

    goto/16 :goto_2

    :cond_5
    const/16 v5, 0x8

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/b/h;->n(I)Z

    move-result v5

    if-eqz v5, :cond_6

    const/4 v5, 0x1

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/b/h;->U:B

    move v6, v0

    if-ne v5, v6, :cond_6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->o:La/a/d;

    move-object v5, v0

    move-object v0, v5

    move v1, v15

    move v2, v14

    move-object/from16 v3, p1

    invoke-virtual {v0, v1, v2, v3}, La/a/d;->a(IILjavax/microedition/lcdui/Graphics;)V

    goto/16 :goto_2

    :cond_6
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->o:La/a/d;

    move-object v5, v0

    move-object v0, v5

    move v1, v15

    move v2, v14

    move-object/from16 v3, p1

    invoke-virtual {v0, v1, v2, v3}, La/a/d;->b(IILjavax/microedition/lcdui/Graphics;)V

    goto/16 :goto_2

    :cond_7
    sget-object v5, Lpmsj/work/b/h;->aa:Lpmsj/work/a/i;

    sub-int v8, v11, v19

    invoke-virtual/range {p2 .. p2}, Ljava/lang/Integer;->intValue()I

    move-result v9

    const/4 v10, 0x0

    move-object/from16 v6, p1

    move v7, v15

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move/from16 v5, v19

    goto :goto_4

    :cond_8
    move-object/from16 v0, p0

    move-object/from16 v1, p1

    move v2, v15

    move v3, v14

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/h;->a(Ljavax/microedition/lcdui/Graphics;II)V

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/b/h;->t()I

    move-result v5

    div-int/lit8 v5, v5, 0x2

    sub-int v5, v14, v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Y:Ljava/util/Vector;

    move-object v6, v0

    invoke-virtual {v6}, Ljava/util/Vector;->size()I

    move-result v6

    const/4 v7, 0x1

    sub-int/2addr v6, v7

    :goto_5
    if-ltz v6, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Y:Ljava/util/Vector;

    move-object v7, v0

    invoke-virtual {v7, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lpmsj/work/b/s;

    invoke-virtual/range {p2 .. p2}, Lpmsj/work/b/s;->f()I

    move-result v7

    shr-int/lit8 v7, v7, 0x1

    sub-int v7, v15, v7

    const/4 v8, 0x0

    move-object/from16 v0, p2

    move-object/from16 v1, p1

    move v2, v7

    move v3, v5

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/b/s;->a(Ljavax/microedition/lcdui/Graphics;IIZ)I

    invoke-virtual/range {p2 .. p2}, Lpmsj/work/b/s;->o()Z

    move-result v7

    if-eqz v7, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->Y:Ljava/util/Vector;

    move-object v7, v0

    invoke-virtual {v7, v6}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_9
    add-int/lit8 v6, v6, -0x1

    goto :goto_5

    :cond_a
    move-object/from16 v0, p0

    move-object/from16 v1, p1

    move v2, v15

    move v3, v14

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/h;->d(Ljavax/microedition/lcdui/Graphics;II)V

    const/16 v5, 0x32

    sub-int v5, v15, v5

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/b/h;->t()I

    move-result v6

    div-int/lit8 v6, v6, 0x2

    sub-int v6, v14, v6

    const/16 v7, 0x14

    sub-int/2addr v6, v7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->W:Ljava/util/Vector;

    move-object v7, v0

    invoke-virtual {v7}, Ljava/util/Vector;->size()I

    move-result v7

    const/4 v8, 0x1

    sub-int/2addr v7, v8

    move/from16 v20, v7

    move v7, v6

    move/from16 v6, v20

    :goto_6
    if-ltz v6, :cond_c

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->W:Ljava/util/Vector;

    move-object v8, v0

    invoke-virtual {v8, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lpmsj/work/d/d;

    int-to-short v8, v5

    move v0, v8

    move-object/from16 v1, p2

    iput-short v0, v1, Lpmsj/work/d/b;->i:S

    int-to-short v8, v7

    move v0, v8

    move-object/from16 v1, p2

    iput-short v0, v1, Lpmsj/work/d/b;->j:S

    const/4 v8, -0x1

    const/4 v9, -0x1

    move-object/from16 v0, p2

    move-object/from16 v1, p1

    move v2, v8

    move v3, v9

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    add-int/lit8 v7, v7, 0xf

    invoke-virtual/range {p2 .. p2}, Lpmsj/work/d/d;->e()Z

    move-result v8

    if-eqz v8, :cond_b

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->W:Ljava/util/Vector;

    move-object v8, v0

    invoke-virtual {v8, v6}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_b
    add-int/lit8 v6, v6, -0x1

    goto :goto_6

    :cond_c
    const/16 v5, 0x32

    sub-int v5, v15, v5

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/b/h;->t()I

    move-result v6

    div-int/lit8 v6, v6, 0x2

    sub-int v6, v14, v6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->X:Ljava/util/Vector;

    move-object v7, v0

    invoke-virtual {v7}, Ljava/util/Vector;->size()I

    move-result v7

    const/4 v8, 0x0

    move/from16 v20, v8

    move v8, v6

    move/from16 v6, v20

    :goto_7
    if-ge v6, v7, :cond_e

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->X:Ljava/util/Vector;

    move-object v9, v0

    invoke-virtual {v9, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lpmsj/work/d/d;

    int-to-short v9, v5

    move v0, v9

    move-object/from16 v1, p2

    iput-short v0, v1, Lpmsj/work/d/b;->i:S

    int-to-short v9, v8

    move v0, v9

    move-object/from16 v1, p2

    iput-short v0, v1, Lpmsj/work/d/b;->j:S

    const/4 v9, -0x1

    const/4 v10, -0x1

    move-object/from16 v0, p2

    move-object/from16 v1, p1

    move v2, v9

    move v3, v10

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    add-int/lit8 v8, v8, 0xf

    invoke-virtual/range {p2 .. p2}, Lpmsj/work/d/d;->e()Z

    move-result v9

    if-eqz v9, :cond_d

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/b/h;->X:Ljava/util/Vector;

    move-object v9, v0

    invoke-virtual {v9, v6}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_d
    add-int/lit8 v6, v6, 0x1

    goto :goto_7

    :cond_e
    return v13
.end method

.method public final c()I
    .locals 1

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    return v0
.end method

.method public final c(B)V
    .locals 6

    iget-short v2, p0, Lpmsj/work/b/h;->w:S

    iget-short v3, p0, Lpmsj/work/b/h;->x:S

    const/4 v4, 0x0

    const/4 v5, 0x0

    move-object v0, p0

    move v1, p1

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/b/h;->a(BSSILjava/lang/String;)V

    return-void
.end method

.method public final c(I)V
    .locals 1

    iget v0, p0, Lpmsj/work/b/h;->T:I

    add-int/2addr v0, p1

    iput v0, p0, Lpmsj/work/b/h;->T:I

    return-void
.end method

.method public final d(B)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lez v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->lastElement()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, La/c/a;->a(I)I

    move-result v0

    if-ne p1, v0, :cond_0

    :goto_0
    return-void

    :cond_0
    invoke-virtual {p0, p1}, Lpmsj/work/b/h;->c(B)V

    goto :goto_0
.end method

.method public final d(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    if-nez v0, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    const/4 v0, 0x1

    const/4 v1, 0x7

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_2

    invoke-super {p0, p1}, Lpmsj/work/b/v;->d(I)V

    goto :goto_0

    :cond_2
    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    sget-byte v1, La/a/d;->e:B

    invoke-virtual {v0, v1}, La/a/d;->c(I)I

    move-result v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/b/h;->o:La/a/d;

    sget-byte v2, La/a/d;->e:B

    add-int/2addr v0, p1

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public final d()Z
    .locals 1

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    if-gtz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final e()I
    .locals 6

    const/4 v5, 0x3

    const/4 v4, 0x2

    const/4 v3, 0x0

    const/4 v2, 0x1

    const/4 v0, 0x5

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    iget-byte v1, v1, Lpmsj/work/main/b;->d:B

    if-ne v5, v1, :cond_2

    if-ne v4, v0, :cond_0

    move v0, v3

    :goto_0
    return v0

    :cond_0
    if-ne v2, v0, :cond_1

    move v0, v2

    goto :goto_0

    :cond_1
    if-ne v5, v0, :cond_2

    move v0, v4

    goto :goto_0

    :cond_2
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    iget-byte v1, v1, Lpmsj/work/main/b;->d:B

    if-ne v0, v1, :cond_3

    move v0, v3

    goto :goto_0

    :cond_3
    move v0, v2

    goto :goto_0
.end method

.method public final e(I)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    const/4 v0, 0x1

    const/4 v1, 0x7

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_1

    invoke-super {p0, p1}, Lpmsj/work/b/v;->e(I)V

    goto :goto_0

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    invoke-virtual {v0, p1}, La/a/d;->b(I)V

    goto :goto_0
.end method

.method public final f()Z
    .locals 9

    const/4 v8, 0x5

    const/4 v7, 0x1

    const/4 v6, 0x0

    iget-boolean v0, p0, Lpmsj/work/b/h;->R:Z

    if-eqz v0, :cond_0

    new-instance v0, La/c/p;

    const-string v1, "[2]Fighter: process : \u5df2\u7ecf\u88ab\u8bbe\u7f6e\u4e3a\u8981\u6700\u540e\u5220\u9664\u7684\u5bf9\u8c61\u8fd8\u5728\u88ab\u5904\u7406"

    invoke-direct {v0, v1}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static {v0}, Lpmsj/work/main/w;->a(La/c/i;)V

    move v0, v7

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    if-nez v0, :cond_1

    move v0, v7

    goto :goto_0

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/h;->o:La/a/d;

    invoke-virtual {v0}, La/a/d;->c()Z

    move-result v0

    if-nez v0, :cond_2

    move v0, v6

    goto :goto_0

    :cond_2
    iget-object v0, p0, Lpmsj/work/b/h;->P:La/c/q;

    invoke-virtual {v0}, La/c/q;->h()Z

    move-result v0

    if-eqz v0, :cond_3

    iget-object v0, p0, Lpmsj/work/b/h;->P:La/c/q;

    invoke-virtual {v0}, La/c/q;->i()Z

    move-result v0

    if-eqz v0, :cond_6

    iget-object v0, p0, Lpmsj/work/b/h;->N:La/b/c;

    iget-object v1, p0, Lpmsj/work/b/h;->O:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    iget-object v2, p0, Lpmsj/work/b/h;->O:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    invoke-virtual {v0, v1, v2}, La/b/c;->a(II)V

    :cond_3
    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lez v0, :cond_7

    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->firstElement()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    iget-object v1, v0, La/c/a;->a:[La/c/i;

    const/4 v4, 0x4

    aget-object v1, v1, v4

    check-cast v1, La/c/n;

    iget-wide v4, v1, La/c/n;->a:J

    cmp-long v1, v2, v4

    if-lez v1, :cond_5

    invoke-virtual {v0, v6}, La/c/a;->a(I)I

    move-result v1

    invoke-virtual {v0, v7}, La/c/a;->a(I)I

    move-result v2

    const/4 v3, 0x2

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v3

    const/4 v4, 0x3

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v4

    invoke-virtual {p0, v1, v2, v3, v4}, Lpmsj/work/b/h;->a(IIII)V

    iget-object v1, v0, La/c/a;->a:[La/c/i;

    aget-object v1, v1, v8

    if-eqz v1, :cond_4

    invoke-virtual {v0, v8}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->b(Ljava/lang/String;)V

    :cond_4
    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0, v6}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_5
    move v0, v6

    goto :goto_0

    :cond_6
    move v0, v6

    goto :goto_0

    :cond_7
    iget-object v0, p0, Lpmsj/work/b/h;->l:Lpmsj/work/b/d;

    if-eqz v0, :cond_8

    iget-object v0, p0, Lpmsj/work/b/h;->l:Lpmsj/work/b/d;

    invoke-virtual {v0}, Lpmsj/work/b/d;->b()I

    move-result v0

    if-lez v0, :cond_8

    move v0, v6

    goto/16 :goto_0

    :cond_8
    iget-object v0, p0, Lpmsj/work/b/h;->m:Lpmsj/work/b/d;

    if-eqz v0, :cond_9

    iget-object v0, p0, Lpmsj/work/b/h;->m:Lpmsj/work/b/d;

    invoke-virtual {v0}, Lpmsj/work/b/d;->b()I

    move-result v0

    if-lez v0, :cond_9

    move v0, v6

    goto/16 :goto_0

    :cond_9
    move v0, v7

    goto/16 :goto_0
.end method

.method public final g()La/b/c;
    .locals 3

    new-instance v0, La/b/c;

    iget-short v1, p0, Lpmsj/work/b/h;->w:S

    iget-short v2, p0, Lpmsj/work/b/h;->x:S

    invoke-direct {v0, v1, v2}, La/b/c;-><init>(II)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v1

    if-nez v1, :cond_1

    sget-object v1, Lpmsj/work/b/h;->L:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    neg-int v1, v1

    sget-object v2, Lpmsj/work/b/h;->L:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    neg-int v2, v2

    invoke-virtual {v0, v1, v2}, La/b/c;->b(II)V

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    const/4 v1, 0x1

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v2

    if-ne v1, v2, :cond_0

    sget-object v1, Lpmsj/work/b/h;->L:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    sget-object v2, Lpmsj/work/b/h;->L:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    invoke-virtual {v0, v1, v2}, La/b/c;->b(II)V

    goto :goto_0
.end method

.method public final g(I)V
    .locals 4

    const/16 v3, 0xa

    new-instance v0, Lpmsj/work/d/d;

    const/16 v1, 0x64

    const v2, 0x5a5c1a

    invoke-direct {v0, v1, v3, v2}, Lpmsj/work/d/d;-><init>(III)V

    const/high16 v1, 0x800000

    sget-byte v2, Lpmsj/work/d/d;->a:B

    or-int/2addr v1, v2

    invoke-virtual {v0, v1}, Lpmsj/work/d/d;->l(I)V

    invoke-virtual {v0, p1}, Lpmsj/work/d/d;->a(I)V

    invoke-virtual {v0}, Lpmsj/work/d/d;->c()V

    iget-object v1, p0, Lpmsj/work/b/h;->X:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-virtual {p0, v3}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    add-int/2addr v0, p1

    const/4 v1, 0x0

    invoke-static {v1, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    const/16 v1, 0xc

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    iget v2, p0, Lpmsj/work/b/h;->T:I

    add-int/2addr v1, v2

    invoke-static {v0, v1}, Ljava/lang/Math;->min(II)I

    move-result v0

    invoke-virtual {p0, v3, v0}, Lpmsj/work/b/h;->a(BI)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->u()I

    move-result v2

    if-ne v1, v2, :cond_2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    const/16 v2, 0x2a

    invoke-virtual {v1, v2, v0}, Lpmsj/work/b/ab;->a(BI)V

    :cond_0
    :goto_0
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    iget-byte v1, v1, Lpmsj/work/main/b;->d:B

    const/4 v2, 0x3

    if-eq v1, v2, :cond_1

    const/4 v1, 0x5

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    iget-byte v2, v2, Lpmsj/work/main/b;->d:B

    if-ne v1, v2, :cond_1

    const/4 v1, 0x1

    const/4 v2, 0x7

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    if-ne v1, v2, :cond_1

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    invoke-static {v1}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v1

    if-eqz v1, :cond_1

    const/4 v2, 0x6

    aget-object v1, v1, v2

    invoke-virtual {v1, v0}, La/c/i;->a(I)V

    :cond_1
    return-void

    :cond_2
    sget-object v1, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-eqz v1, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    invoke-virtual {v2}, Lpmsj/work/b/u;->u()I

    move-result v2

    if-ne v1, v2, :cond_0

    sget-object v1, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v2, 0x28

    invoke-virtual {v1, v2, v0}, Lpmsj/work/b/u;->a(BI)V

    goto :goto_0
.end method

.method public final h()La/b/c;
    .locals 3

    new-instance v0, La/b/c;

    iget-short v1, p0, Lpmsj/work/b/h;->w:S

    iget-short v2, p0, Lpmsj/work/b/h;->x:S

    invoke-direct {v0, v1, v2}, La/b/c;-><init>(II)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v1

    if-nez v1, :cond_1

    sget-object v1, Lpmsj/work/b/h;->M:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    neg-int v1, v1

    sget-object v2, Lpmsj/work/b/h;->M:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    neg-int v2, v2

    invoke-virtual {v0, v1, v2}, La/b/c;->b(II)V

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    const/4 v1, 0x1

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v2

    if-ne v1, v2, :cond_0

    sget-object v1, Lpmsj/work/b/h;->M:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    sget-object v2, Lpmsj/work/b/h;->M:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    invoke-virtual {v0, v1, v2}, La/b/c;->b(II)V

    goto :goto_0
.end method

.method public final h(I)Z
    .locals 4

    const/4 v3, 0x0

    const/4 v2, 0x1

    const/4 v0, 0x7

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :pswitch_0
    move v0, v3

    :goto_0
    return v0

    :pswitch_1
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v0

    if-nez v0, :cond_4

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    if-ne v0, v1, :cond_2

    and-int/lit8 v0, p1, 0x4

    if-eqz v0, :cond_1

    move v0, v2

    goto :goto_0

    :cond_1
    move v0, v3

    goto :goto_0

    :cond_2
    and-int/lit8 v0, p1, 0x10

    if-eqz v0, :cond_3

    move v0, v2

    goto :goto_0

    :cond_3
    move v0, v3

    goto :goto_0

    :cond_4
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v0

    if-ne v2, v0, :cond_0

    and-int/lit8 v0, p1, 0x40

    if-eqz v0, :cond_5

    move v0, v2

    goto :goto_0

    :cond_5
    move v0, v3

    goto :goto_0

    :pswitch_2
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v0

    if-nez v0, :cond_9

    sget-object v0, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-eqz v0, :cond_7

    sget-object v0, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v0

    invoke-virtual {p0}, Lpmsj/work/b/h;->u()I

    move-result v1

    if-ne v0, v1, :cond_7

    and-int/lit8 v0, p1, 0x8

    if-eqz v0, :cond_6

    move v0, v2

    goto :goto_0

    :cond_6
    move v0, v3

    goto :goto_0

    :cond_7
    and-int/lit8 v0, p1, 0x20

    if-eqz v0, :cond_8

    move v0, v2

    goto :goto_0

    :cond_8
    move v0, v3

    goto :goto_0

    :cond_9
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v0

    if-ne v2, v0, :cond_0

    and-int/lit16 v0, p1, 0x80

    if-eqz v0, :cond_a

    move v0, v2

    goto :goto_0

    :cond_a
    move v0, v3

    goto :goto_0

    :pswitch_3
    and-int/lit16 v0, p1, 0x100

    if-eqz v0, :cond_b

    move v0, v2

    goto :goto_0

    :cond_b
    and-int/lit16 v0, p1, 0x1000

    if-eqz v0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->a(I)Z

    move-result v0

    if-eqz v0, :cond_0

    move v0, v2

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_2
        :pswitch_0
        :pswitch_3
    .end packed-switch
.end method

.method public final i()V
    .locals 1

    const/4 v0, 0x1

    iput-boolean v0, p0, Lpmsj/work/b/h;->R:Z

    return-void
.end method

.method public final i(I)V
    .locals 3

    div-int/lit8 v0, p1, 0x64

    mul-int/lit8 v0, v0, 0x64

    rem-int/lit8 v1, p1, 0x64

    const/4 v2, 0x0

    invoke-virtual {p0, v0, v1, v2}, Lpmsj/work/b/h;->a(IIZ)La/a/d;

    return-void
.end method

.method public final j(I)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    if-nez v0, :cond_0

    new-instance v0, Ljava/util/Vector;

    const/4 v1, 0x1

    invoke-direct {v0, v1}, Ljava/util/Vector;-><init>(I)V

    iput-object v0, p0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    new-instance v1, Ljava/lang/Integer;

    invoke-direct {v1, p1}, Ljava/lang/Integer;-><init>(I)V

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    return-void
.end method

.method public final j()Z
    .locals 1

    iget-boolean v0, p0, Lpmsj/work/b/h;->R:Z

    return v0
.end method

.method public final k()B
    .locals 1

    iget-byte v0, p0, Lpmsj/work/b/h;->Q:B

    return v0
.end method

.method public final k(I)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/h;->Z:Ljava/util/Vector;

    new-instance v1, Ljava/lang/Integer;

    invoke-direct {v1, p1}, Ljava/lang/Integer;-><init>(I)V

    invoke-virtual {v0, v1}, Ljava/util/Vector;->removeElement(Ljava/lang/Object;)Z

    goto :goto_0
.end method

.method public final l()La/b/c;
    .locals 4

    const/4 v1, 0x0

    const/16 v3, -0x14

    new-instance v0, La/b/c;

    invoke-direct {v0, v1, v1}, La/b/c;-><init>(II)V

    const/4 v1, 0x1

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v2

    if-ne v1, v2, :cond_2

    iget-object v1, p0, Lpmsj/work/b/h;->O:La/b/c;

    iget-short v1, v1, La/b/c;->a:S

    iget-object v2, p0, Lpmsj/work/b/h;->O:La/b/c;

    iget-short v2, v2, La/b/c;->b:S

    if-le v1, v2, :cond_1

    sget-short v1, Lpmsj/work/main/t;->d:S

    div-int/lit8 v1, v1, 0x2

    invoke-static {v1}, La/c/x;->a(I)I

    move-result v1

    invoke-virtual {v0, v3, v1}, La/b/c;->a(II)V

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    sget-short v1, Lpmsj/work/main/t;->c:S

    mul-int/lit8 v1, v1, 0x2

    div-int/lit8 v1, v1, 0x3

    invoke-virtual {v0, v1, v3}, La/b/c;->a(II)V

    goto :goto_0

    :cond_2
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v1

    if-nez v1, :cond_0

    iget-object v1, p0, Lpmsj/work/b/h;->O:La/b/c;

    iget-short v1, v1, La/b/c;->b:S

    sget-short v2, Lpmsj/work/main/t;->d:S

    if-lt v1, v2, :cond_3

    sget-short v1, Lpmsj/work/main/t;->c:S

    add-int/lit8 v1, v1, 0x14

    sget-short v2, Lpmsj/work/main/t;->d:S

    div-int/lit8 v2, v2, 0x2

    sget-short v3, Lpmsj/work/main/t;->d:S

    invoke-static {v2, v3}, La/c/x;->a(II)I

    move-result v2

    invoke-virtual {v0, v1, v2}, La/b/c;->a(II)V

    goto :goto_0

    :cond_3
    sget-short v1, Lpmsj/work/main/t;->c:S

    div-int/lit8 v1, v1, 0x3

    sget-short v2, Lpmsj/work/main/t;->c:S

    invoke-static {v1, v2}, La/c/x;->a(II)I

    move-result v1

    sget-short v2, Lpmsj/work/main/t;->d:S

    add-int/lit8 v2, v2, 0x14

    invoke-virtual {v0, v1, v2}, La/b/c;->a(II)V

    goto :goto_0
.end method

.method public final l(I)V
    .locals 3

    const/4 v2, 0x0

    iget v0, p0, Lpmsj/work/b/h;->ab:I

    or-int/2addr v0, p1

    iput v0, p0, Lpmsj/work/b/h;->ab:I

    and-int/lit8 v0, p1, 0x4

    if-eqz v0, :cond_1

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    if-eqz v0, :cond_1

    const/4 v0, 0x1

    const/4 v1, 0x7

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_0

    invoke-static {v2}, Lpmsj/work/b/h;->f(I)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->o(I)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->r()V

    :cond_0
    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->e(I)V

    iget-byte v0, p0, Lpmsj/work/b/h;->U:B

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->b(B)V

    :cond_1
    return-void
.end method

.method public final m()La/b/c;
    .locals 5

    const/4 v2, 0x0

    const/4 v3, 0x1

    const/4 v0, 0x2

    invoke-static {v0}, La/c/x;->a(I)I

    move-result v0

    new-instance v1, La/b/c;

    invoke-direct {v1, v2, v2}, La/b/c;-><init>(II)V

    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v2

    if-ne v3, v2, :cond_2

    if-ne v0, v3, :cond_1

    sget-byte v0, Lpmsj/work/b/m;->k:B

    sget-short v2, Lpmsj/work/main/t;->d:S

    div-int/lit8 v2, v2, 0x2

    invoke-static {v2}, La/c/x;->a(I)I

    move-result v2

    invoke-virtual {v1, v0, v2}, La/b/c;->a(II)V

    :cond_0
    :goto_0
    return-object v1

    :cond_1
    sget-short v0, Lpmsj/work/main/t;->c:S

    mul-int/lit8 v0, v0, 0x2

    div-int/lit8 v0, v0, 0x3

    invoke-virtual {p0}, Lpmsj/work/b/h;->t()I

    move-result v2

    invoke-virtual {v1, v0, v2}, La/b/c;->a(II)V

    goto :goto_0

    :cond_2
    invoke-virtual {p0}, Lpmsj/work/b/h;->e()I

    move-result v2

    if-nez v2, :cond_0

    if-ne v0, v3, :cond_3

    sget-short v0, Lpmsj/work/main/t;->c:S

    sget-short v2, Lpmsj/work/main/t;->d:S

    div-int/lit8 v2, v2, 0x2

    sget-short v3, Lpmsj/work/main/t;->d:S

    sget-byte v4, Lpmsj/work/b/m;->k:B

    sub-int/2addr v3, v4

    invoke-static {v2, v3}, La/c/x;->a(II)I

    move-result v2

    invoke-virtual {v1, v0, v2}, La/b/c;->a(II)V

    goto :goto_0

    :cond_3
    sget-short v0, Lpmsj/work/main/t;->c:S

    div-int/lit8 v0, v0, 0x3

    sget-short v2, Lpmsj/work/main/t;->c:S

    invoke-static {v0, v2}, La/c/x;->a(II)I

    move-result v0

    sget-short v2, Lpmsj/work/main/t;->d:S

    invoke-virtual {v1, v0, v2}, La/b/c;->a(II)V

    goto :goto_0
.end method

.method public final m(I)V
    .locals 3

    iget v0, p0, Lpmsj/work/b/h;->ab:I

    xor-int/lit8 v1, p1, -0x1

    and-int/2addr v0, v1

    iput v0, p0, Lpmsj/work/b/h;->ab:I

    and-int/lit8 v0, p1, 0x4

    if-eqz v0, :cond_1

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    if-eqz v0, :cond_1

    const/4 v1, 0x1

    const/4 v2, 0x7

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    if-ne v1, v2, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/h;->A()V

    invoke-virtual {p0}, Lpmsj/work/b/h;->r()V

    :cond_0
    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->e(I)V

    iget-byte v0, p0, Lpmsj/work/b/h;->U:B

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->b(B)V

    :cond_1
    return-void
.end method

.method public final n()I
    .locals 1

    iget v0, p0, Lpmsj/work/b/h;->S:I

    return v0
.end method

.method public final n(I)Z
    .locals 1

    iget v0, p0, Lpmsj/work/b/h;->ab:I

    and-int/2addr v0, p1

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final o()I
    .locals 1

    iget v0, p0, Lpmsj/work/b/h;->T:I

    return v0
.end method

.method public final p()Ljava/lang/String;
    .locals 2

    const/4 v1, 0x6

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->a(I)Z

    move-result v0

    if-eqz v0, :cond_0

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->j(B)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "(\u5b9d\u5b9d)"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    :goto_0
    return-object v0

    :cond_0
    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->j(B)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method public final q()Z
    .locals 2

    const/4 v1, 0x1

    const/16 v0, 0x15

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/h;->x(I)B

    move-result v0

    if-ne v1, v0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final r()V
    .locals 3

    const/16 v2, 0x15

    const/16 v0, 0xd

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->d(I)V

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->e(I)V

    const/4 v0, 0x1

    const/4 v1, 0x7

    invoke-virtual {p0, v1}, Lpmsj/work/b/h;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->y(I)V

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->M(I)V

    const/16 v0, 0xe

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->z(I)V

    const/16 v0, 0xf

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->A(I)V

    const/16 v0, 0x10

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->B(I)V

    const/16 v0, 0x11

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->C(I)V

    const/16 v0, 0x12

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->D(I)V

    const/16 v0, 0x13

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->E(I)V

    const/16 v0, 0x14

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/h;->F(I)V

    :cond_0
    return-void
.end method

.method public final s()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/h;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    return-void
.end method
