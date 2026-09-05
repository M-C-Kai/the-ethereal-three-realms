.class public Lpmsj/work/b/n;
.super Lpmsj/work/b/e;


# static fields
.field public static r:La/a/d;


# instance fields
.field private h:Ljava/lang/String;

.field private i:I

.field public j:I

.field public k:Ljava/lang/String;

.field protected l:Lpmsj/work/b/d;

.field protected m:Lpmsj/work/b/d;

.field public n:B

.field public o:La/a/d;

.field public p:Ljava/util/Vector;

.field protected q:B

.field public s:I

.field public t:I

.field public u:I

.field public v:Z

.field public w:S

.field public x:S

.field public y:Z

.field protected z:Lpmsj/work/b/ac;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    const v0, 0x203230

    const/4 v1, 0x0

    invoke-static {v0, v1}, La/a/d;->a(IZ)La/a/d;

    move-result-object v0

    sput-object v0, Lpmsj/work/b/n;->r:La/a/d;

    return-void
.end method

.method public constructor <init>(IIZZ)V
    .locals 1

    invoke-direct {p0}, Lpmsj/work/b/e;-><init>()V

    const-string v0, ""

    iput-object v0, p0, Lpmsj/work/b/n;->k:Ljava/lang/String;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    sget v0, Lpmsj/work/a/c;->y:I

    iput v0, p0, Lpmsj/work/b/n;->s:I

    iput p1, p0, Lpmsj/work/b/n;->j:I

    iput p2, p0, Lpmsj/work/b/n;->u:I

    iput-boolean p3, p0, Lpmsj/work/b/n;->v:Z

    invoke-virtual {p0}, Lpmsj/work/b/n;->A()V

    if-eqz p4, :cond_0

    new-instance v0, Lpmsj/work/b/ac;

    invoke-direct {v0}, Lpmsj/work/b/ac;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    :cond_0
    return-void
.end method


# virtual methods
.method public A()V
    .locals 1

    iget v0, p0, Lpmsj/work/b/n;->u:I

    invoke-virtual {p0, v0}, Lpmsj/work/b/n;->o(I)V

    return-void
.end method

.method public final B()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    return-void
.end method

.method public final C()I
    .locals 1

    iget-byte v0, p0, Lpmsj/work/b/n;->q:B

    mul-int/lit8 v0, v0, 0x6

    return v0
.end method

.method public final D()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->f()V

    invoke-virtual {p0}, Lpmsj/work/b/n;->I()V

    return-void
.end method

.method public final E()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->f()V

    return-void
.end method

.method public F()La/a/d;
    .locals 2

    invoke-virtual {p0}, Lpmsj/work/b/n;->v()I

    move-result v0

    iget-boolean v1, p0, Lpmsj/work/b/n;->v:Z

    invoke-static {v0, v1}, La/a/d;->a(IZ)La/a/d;

    move-result-object v0

    return-object v0
.end method

.method public G()V
    .locals 1

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    return-void
.end method

.method public final H()La/a/d;
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    return-object v0
.end method

.method public I()V
    .locals 5

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    const/4 v0, 0x3

    iget-byte v1, p0, Lpmsj/work/b/n;->n:B

    if-ne v0, v1, :cond_1

    const/4 v0, 0x2

    iget-byte v1, p0, Lpmsj/work/b/n;->q:B

    mul-int/lit8 v1, v1, 0x6

    add-int/lit8 v1, v1, 0x1

    move v4, v1

    move v1, v0

    move v0, v4

    :goto_1
    iget-object v2, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v2, v1}, La/a/d;->a(B)V

    iget-object v1, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v1, v0}, La/a/d;->d(I)V

    iput-boolean v3, p0, Lpmsj/work/b/n;->y:Z

    goto :goto_0

    :cond_1
    iget-byte v0, p0, Lpmsj/work/b/n;->q:B

    mul-int/lit8 v0, v0, 0x6

    iget-byte v1, p0, Lpmsj/work/b/n;->n:B

    add-int/2addr v0, v1

    move v1, v3

    goto :goto_1
.end method

.method public J()V
    .locals 5

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    iget-byte v0, p0, Lpmsj/work/b/n;->q:B

    mul-int/lit8 v0, v0, 0x6

    add-int/lit8 v0, v0, 0x3

    const/4 v1, 0x0

    iget-byte v2, p0, Lpmsj/work/b/n;->n:B

    add-int/2addr v2, v0

    const/4 v3, 0x3

    iget-byte v4, p0, Lpmsj/work/b/n;->n:B

    if-ne v3, v4, :cond_1

    const/4 v1, 0x2

    add-int/lit8 v0, v0, 0x1

    :goto_1
    iget-object v2, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v2, v1}, La/a/d;->a(B)V

    iget-object v1, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v1, v0}, La/a/d;->d(I)V

    const/4 v0, 0x1

    iput-boolean v0, p0, Lpmsj/work/b/n;->y:Z

    goto :goto_0

    :cond_1
    move v0, v2

    goto :goto_1
.end method

.method public K()Z
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->i()Z

    move-result v0

    if-nez v0, :cond_1

    const/4 v0, 0x0

    :cond_0
    :goto_0
    return v0

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->j()Z

    move-result v0

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->a()S

    move-result v1

    iput-short v1, p0, Lpmsj/work/b/n;->c:S

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->b()S

    move-result v1

    iput-short v1, p0, Lpmsj/work/b/n;->d:S

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->c()B

    move-result v1

    iput-byte v1, p0, Lpmsj/work/b/n;->e:B

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->d()B

    move-result v1

    iput-byte v1, p0, Lpmsj/work/b/n;->f:B

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->e()B

    move-result v1

    iget-byte v2, p0, Lpmsj/work/b/n;->n:B

    if-ne v1, v2, :cond_2

    iget-boolean v2, p0, Lpmsj/work/b/n;->y:Z

    if-nez v2, :cond_3

    :cond_2
    iput-byte v1, p0, Lpmsj/work/b/n;->n:B

    invoke-virtual {p0}, Lpmsj/work/b/n;->J()V

    :cond_3
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->w()V

    goto :goto_0
.end method

.method public L()Z
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->i()Z

    move-result v0

    return v0
.end method

.method public final M()Z
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->i()Z

    move-result v0

    return v0
.end method

.method final N()V
    .locals 1

    iget-boolean v0, p0, Lpmsj/work/b/n;->y:Z

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/n;->J()V

    :goto_0
    return-void

    :cond_0
    invoke-virtual {p0}, Lpmsj/work/b/n;->I()V

    goto :goto_0
.end method

.method public final O()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->h()V

    return-void
.end method

.method public final a(IIZ)La/a/d;
    .locals 1

    invoke-static {p1}, La/a/d;->e(I)Z

    move-result v0

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/b/d;

    invoke-direct {v0}, Lpmsj/work/b/d;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    invoke-virtual {v0, p1, p2, p3}, Lpmsj/work/b/d;->a(IIZ)La/a/d;

    move-result-object v0

    :goto_0
    return-object v0

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    if-nez v0, :cond_2

    new-instance v0, Lpmsj/work/b/d;

    invoke-direct {v0}, Lpmsj/work/b/d;-><init>()V

    iput-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    :cond_2
    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    invoke-virtual {v0, p1, p2, p3}, Lpmsj/work/b/d;->a(IIZ)La/a/d;

    move-result-object v0

    goto :goto_0
.end method

.method public final a(BI)V
    .locals 1

    new-instance v0, La/c/m;

    invoke-direct {v0, p2}, La/c/m;-><init>(I)V

    invoke-virtual {p0, p1, v0}, Lpmsj/work/b/n;->a(BLjava/lang/Object;)V

    return-void
.end method

.method public final a(BLjava/lang/Object;)V
    .locals 4

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lt p1, v0, :cond_0

    sub-int v0, p1, v0

    add-int/lit8 v0, v0, 0x1

    const/4 v1, 0x0

    :goto_0
    if-ge v1, v0, :cond_0

    iget-object v2, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    const/4 v3, 0x0

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p2, p1}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    return-void
.end method

.method public a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 7

    invoke-virtual {p0}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v1

    iget-object v0, p0, Lpmsj/work/b/n;->h:Ljava/lang/String;

    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    iput-object v1, p0, Lpmsj/work/b/n;->h:Ljava/lang/String;

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/b/n;->i:I

    :cond_0
    iget v0, p0, Lpmsj/work/b/n;->i:I

    div-int/lit8 v0, v0, 0x2

    sub-int v2, p2, v0

    invoke-virtual {p0}, Lpmsj/work/b/n;->t()I

    move-result v0

    sub-int v0, p3, v0

    sget-object v3, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v3}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v3

    sub-int v3, v0, v3

    sget-object v4, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    iget v5, p0, Lpmsj/work/b/n;->s:I

    iget v6, p0, Lpmsj/work/b/n;->t:I

    move-object v0, p1

    invoke-static/range {v0 .. v6}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    return-void
.end method

.method public a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/b/m;)V
    .locals 3

    iget-short v0, p0, Lpmsj/work/b/n;->c:S

    invoke-virtual {p2, v0}, Lpmsj/work/b/m;->g(I)I

    move-result v0

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/b/n;->w:S

    iget-short v0, p0, Lpmsj/work/b/n;->d:S

    invoke-virtual {p2, v0}, Lpmsj/work/b/m;->h(I)I

    move-result v0

    iget-byte v1, p0, Lpmsj/work/b/n;->e:B

    iget-byte v2, p0, Lpmsj/work/b/n;->f:B

    invoke-virtual {p2, v1, v2}, Lpmsj/work/b/m;->f(II)I

    move-result v1

    sub-int/2addr v0, v1

    int-to-short v0, v0

    iput-short v0, p0, Lpmsj/work/b/n;->x:S

    iget-short v0, p0, Lpmsj/work/b/n;->w:S

    iget-short v1, p0, Lpmsj/work/b/n;->x:S

    invoke-virtual {p0, p2, p1, v0, v1}, Lpmsj/work/b/n;->a(Lpmsj/work/b/m;Ljavax/microedition/lcdui/Graphics;II)V

    iget-object v0, p0, Lpmsj/work/b/n;->k:Ljava/lang/String;

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v0

    if-lez v0, :cond_0

    iget-short v0, p0, Lpmsj/work/b/n;->w:S

    iget-short v1, p0, Lpmsj/work/b/n;->x:S

    invoke-virtual {p0, p1, v0, v1}, Lpmsj/work/b/n;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_0
    return-void
.end method

.method public a(Lpmsj/work/b/m;Ljavax/microedition/lcdui/Graphics;II)V
    .locals 2

    invoke-virtual {p1}, Lpmsj/work/b/m;->g()Lpmsj/work/b/n;

    move-result-object v0

    if-ne v0, p0, :cond_0

    sget-object v1, Lpmsj/work/b/n;->r:La/a/d;

    invoke-virtual {v1, p3, p4, p2}, La/a/d;->b(IILjavax/microedition/lcdui/Graphics;)V

    :cond_0
    iget-object v1, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-eqz v1, :cond_1

    iget-object v1, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v1, p3, p4, p2}, La/a/d;->b(IILjavax/microedition/lcdui/Graphics;)V

    :cond_1
    if-ne v0, p0, :cond_2

    iget-byte v0, p0, Lpmsj/work/b/n;->g:B

    const/4 v1, 0x1

    if-eq v0, v1, :cond_2

    iget-byte v0, p0, Lpmsj/work/b/n;->g:B

    const/16 v1, 0x8

    if-eq v0, v1, :cond_2

    invoke-virtual {p0, p2, p3, p4}, Lpmsj/work/b/n;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_2
    return-void
.end method

.method public a(I)Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public b(IIZ)I
    .locals 6

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    iget-byte v1, p0, Lpmsj/work/b/n;->e:B

    iget-byte v2, p0, Lpmsj/work/b/n;->f:B

    move v3, p1

    move v4, p2

    move v5, p3

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/b/ac;->a(IIIIZ)I

    move-result v0

    if-lez v0, :cond_2

    iget-object v1, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v1}, Lpmsj/work/b/ac;->e()B

    move-result v1

    iget-boolean v2, p0, Lpmsj/work/b/n;->y:Z

    if-eqz v2, :cond_0

    iget-byte v2, p0, Lpmsj/work/b/n;->n:B

    if-eq v2, v1, :cond_1

    :cond_0
    iput-byte v1, p0, Lpmsj/work/b/n;->n:B

    invoke-virtual {p0}, Lpmsj/work/b/n;->J()V

    :cond_1
    :goto_0
    return v0

    :cond_2
    iget-boolean v1, p0, Lpmsj/work/b/n;->y:Z

    if-eqz v1, :cond_1

    invoke-virtual {p0}, Lpmsj/work/b/n;->I()V

    goto :goto_0
.end method

.method public final b(IZ)La/a/d;
    .locals 2

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0, p2}, Lpmsj/work/b/n;->a(IIZ)La/a/d;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/n;->t()I

    move-result v1

    neg-int v1, v1

    invoke-virtual {v0, v1}, La/a/d;->a(I)V

    :cond_0
    return-object v0
.end method

.method public c()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final c(IZ)La/a/d;
    .locals 1

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0, p2}, Lpmsj/work/b/n;->a(IIZ)La/a/d;

    move-result-object v0

    return-object v0
.end method

.method public c(II)V
    .locals 3

    int-to-byte v0, p1

    iput-byte v0, p0, Lpmsj/work/b/n;->e:B

    int-to-byte v0, p2

    iput-byte v0, p0, Lpmsj/work/b/n;->f:B

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    iget-byte v1, p0, Lpmsj/work/b/n;->e:B

    iget-byte v2, p0, Lpmsj/work/b/n;->f:B

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/m;->g(II)La/b/c;

    move-result-object v0

    iget-short v1, v0, La/b/c;->a:S

    iput-short v1, p0, Lpmsj/work/b/n;->c:S

    iget-short v0, v0, La/b/c;->b:S

    iput-short v0, p0, Lpmsj/work/b/n;->d:S

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->z:Lpmsj/work/b/ac;

    invoke-virtual {v0}, Lpmsj/work/b/ac;->f()V

    :cond_0
    return-void
.end method

.method public final c(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    invoke-virtual {v0, p1, p2, p3}, Lpmsj/work/b/d;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_0
    return-void
.end method

.method public final d(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    invoke-virtual {v0, p1, p2, p3}, Lpmsj/work/b/d;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_0
    return-void
.end method

.method public final d(II)Z
    .locals 1

    invoke-virtual {p0, p2}, Lpmsj/work/b/n;->a(I)Z

    move-result v0

    if-nez v0, :cond_0

    and-int v0, p1, p2

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final e(B)V
    .locals 0

    iput-byte p1, p0, Lpmsj/work/b/n;->q:B

    return-void
.end method

.method public final e(II)Z
    .locals 1

    invoke-virtual {p0, p2}, Lpmsj/work/b/n;->a(I)Z

    move-result v0

    if-eqz v0, :cond_0

    and-int v0, p1, p2

    if-nez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final f(B)I
    .locals 2

    const/4 v1, 0x0

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    if-nez p0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    invoke-virtual {p0}, La/c/i;->b()I

    move-result v0

    goto :goto_0

    :cond_1
    move v0, v1

    goto :goto_0
.end method

.method public final f(II)V
    .locals 5

    const v0, 0x2dc6c0

    move v1, p2

    move v2, p1

    :goto_0
    if-gtz v2, :cond_0

    if-lez v1, :cond_3

    :cond_0
    add-int/lit8 v0, v0, 0x1

    and-int/lit8 v3, v2, 0x1

    if-eqz v3, :cond_2

    and-int/lit8 v3, v1, 0x1

    if-nez v3, :cond_2

    const/4 v3, 0x0

    const/4 v4, 0x1

    invoke-virtual {p0, v0, v3, v4}, Lpmsj/work/b/n;->a(IIZ)La/a/d;

    :cond_1
    :goto_1
    shr-int/lit8 v2, v2, 0x1

    shr-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_2
    and-int/lit8 v3, v2, 0x1

    if-nez v3, :cond_1

    and-int/lit8 v3, v1, 0x1

    if-eqz v3, :cond_1

    invoke-virtual {p0, v0}, Lpmsj/work/b/n;->t(I)V

    goto :goto_1

    :cond_3
    return-void
.end method

.method public final g(B)J
    .locals 3

    const-wide/16 v1, 0x0

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    if-nez p0, :cond_0

    move-wide v0, v1

    :goto_0
    return-wide v0

    :cond_0
    invoke-virtual {p0}, La/c/i;->c()J

    move-result-wide v0

    goto :goto_0

    :cond_1
    move-wide v0, v1

    goto :goto_0
.end method

.method public final g(II)V
    .locals 2

    const v0, 0x2dc6c0

    if-le p1, v0, :cond_0

    const/4 v0, 0x0

    const/4 v1, 0x1

    invoke-virtual {p0, p1, v0, v1}, Lpmsj/work/b/n;->a(IIZ)La/a/d;

    :goto_0
    return-void

    :cond_0
    invoke-virtual {p0, p2}, Lpmsj/work/b/n;->t(I)V

    goto :goto_0
.end method

.method public final h(B)F
    .locals 2

    const/4 v1, 0x0

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    if-nez p0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    invoke-virtual {p0}, La/c/i;->b()I

    move-result v0

    int-to-float v0, v0

    goto :goto_0

    :cond_1
    move v0, v1

    goto :goto_0
.end method

.method public final i(B)Z
    .locals 2

    const/4 v1, 0x0

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    move v0, v1

    goto :goto_0

    :cond_1
    move v0, v1

    goto :goto_0
.end method

.method public final j(B)Ljava/lang/String;
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge p1, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->p:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/i;

    invoke-virtual {p0}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v0

    :goto_0
    return-object v0

    :cond_0
    const-string v0, ""

    goto :goto_0
.end method

.method protected final o(I)V
    .locals 1

    if-eqz p1, :cond_0

    iget-boolean v0, p0, Lpmsj/work/b/n;->v:Z

    invoke-static {p1, v0}, La/a/d;->a(IZ)La/a/d;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    :cond_0
    return-void
.end method

.method public p()Ljava/lang/String;
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->k:Ljava/lang/String;

    return-object v0
.end method

.method public final p(I)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v0, p1}, La/a/d;->d(I)V

    :cond_0
    return-void
.end method

.method public final q(I)V
    .locals 1

    int-to-byte v0, p1

    iput-byte v0, p0, Lpmsj/work/b/n;->n:B

    return-void
.end method

.method public final r(I)V
    .locals 1

    iput p1, p0, Lpmsj/work/b/n;->s:I

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/b/n;->t:I

    return-void
.end method

.method public final s(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-nez v0, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    sget-byte v1, La/a/d;->e:B

    invoke-virtual {v0, v1}, La/a/d;->c(I)I

    move-result v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/b/n;->o:La/a/d;

    sget-byte v2, La/a/d;->e:B

    add-int/2addr v0, p1

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public final t()I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->o:La/a/d;

    invoke-virtual {v0}, La/a/d;->e()I

    move-result v0

    :goto_0
    return v0

    :cond_0
    const/16 v0, 0x32

    goto :goto_0
.end method

.method public final t(I)V
    .locals 1

    const v0, 0x9c40

    if-gt v0, p1, :cond_1

    const v0, 0xc350

    if-ge p1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->m:Lpmsj/work/b/d;

    invoke-virtual {v0, p1}, Lpmsj/work/b/d;->a(I)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/n;->l:Lpmsj/work/b/d;

    invoke-virtual {v0, p1}, Lpmsj/work/b/d;->a(I)V

    goto :goto_0
.end method

.method public final u()I
    .locals 1

    iget v0, p0, Lpmsj/work/b/n;->j:I

    return v0
.end method

.method public v()I
    .locals 1

    iget v0, p0, Lpmsj/work/b/n;->u:I

    return v0
.end method

.method public w()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public x()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public y()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public z()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method
